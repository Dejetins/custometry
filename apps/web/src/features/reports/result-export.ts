// Adapted from the preserved pilot spreadsheet serializer; data comes from the active result table.
export type Rows=readonly (readonly (string|number)[])[];
export function spreadsheetSafeValue(value:unknown):string{const text=String(value??'');return /^[\s]*[=+\-@]/.test(text)?"'"+text:text;}
export function rowsToCsv(rows:Rows):string{return '\ufeff'+rows.map(row=>row.map(value=>'"'+(typeof value==='number'?String(value):spreadsheetSafeValue(value)).replaceAll('"','""')+'"').join(',')).join('\r\n');}
    function xmlEscape(value:unknown) {
      return String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&apos;');
    }

    function excelColumnName(index:number) {
      let value = index + 1;
      let name = '';
      while (value) { value -= 1; name = String.fromCharCode(65 + (value % 26)) + name; value = Math.floor(value / 26); }
      return name;
    }

    function worksheetXml(rows:Rows) {
      const columnCount = Math.max(1, ...rows.map(row => row.length));
      const rowCount = Math.max(1, rows.length);
      const columnWidths = Array.from({ length: columnCount }, (_, columnIndex) => Math.min(42, Math.max(10, ...rows.map(row => String(row[columnIndex] ?? '').length + 2))));
      const sheetRows = rows.map((row, rowIndex) => `<row r="${rowIndex + 1}">${row.map((value, columnIndex) => {
        const reference = `${excelColumnName(columnIndex)}${rowIndex + 1}`;
        if (typeof value === 'number' && Number.isFinite(value)) return `<c r="${reference}"><v>${value}</v></c>`;
        return `<c r="${reference}" t="inlineStr"><is><t xml:space="preserve">${xmlEscape(spreadsheetSafeValue(value))}</t></is></c>`;
      }).join('')}</row>`).join('');
      return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><dimension ref="A1:${excelColumnName(columnCount - 1)}${rowCount}"/><sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews><cols>${columnWidths.map((width, index) => `<col min="${index + 1}" max="${index + 1}" width="${width}" customWidth="1"/>`).join('')}</cols><sheetData>${sheetRows}</sheetData><autoFilter ref="A1:${excelColumnName(columnCount - 1)}${rowCount}"/></worksheet>`;
    }

    const crc32Table = Array.from({ length: 256 }, (_, initial) => {
      let value = initial;
      for (let bit = 0; bit < 8; bit += 1) value = (value & 1) ? (0xedb88320 ^ (value >>> 1)) : (value >>> 1);
      return value >>> 0;
    });

    function crc32(bytes:Uint8Array) {
      let value = 0xffffffff;
      bytes.forEach(byte => { value = crc32Table[(value ^ byte) & 0xff] ^ (value >>> 8); });
      return (value ^ 0xffffffff) >>> 0;
    }

    function appendUint16(target:number[], value:number) { target.push(value & 0xff, (value >>> 8) & 0xff); }
    function appendUint32(target:number[], value:number) { target.push(value & 0xff, (value >>> 8) & 0xff, (value >>> 16) & 0xff, (value >>> 24) & 0xff); }

    function storedZip(entries:{name:string;data:string|Uint8Array}[], mimeType:string) {
      const encoder = new TextEncoder();
      const localParts:BlobPart[] = [];
      const centralParts:BlobPart[] = [];
      let offset = 0;
      let centralSize = 0;
      entries.forEach(entry => {
        const name = encoder.encode(entry.name);
        const data = typeof entry.data === 'string' ? encoder.encode(entry.data) : entry.data;
        const checksum = crc32(data);
        const localHeader:number[] = [];
        appendUint32(localHeader, 0x04034b50); appendUint16(localHeader, 20); appendUint16(localHeader, 0); appendUint16(localHeader, 0); appendUint16(localHeader, 0); appendUint16(localHeader, 0x21); appendUint32(localHeader, checksum); appendUint32(localHeader, data.length); appendUint32(localHeader, data.length); appendUint16(localHeader, name.length); appendUint16(localHeader, 0);
        const localBytes = new Uint8Array(localHeader);
        localParts.push(localBytes, name, data);

        const centralHeader:number[] = [];
        appendUint32(centralHeader, 0x02014b50); appendUint16(centralHeader, 20); appendUint16(centralHeader, 20); appendUint16(centralHeader, 0); appendUint16(centralHeader, 0); appendUint16(centralHeader, 0); appendUint16(centralHeader, 0x21); appendUint32(centralHeader, checksum); appendUint32(centralHeader, data.length); appendUint32(centralHeader, data.length); appendUint16(centralHeader, name.length); appendUint16(centralHeader, 0); appendUint16(centralHeader, 0); appendUint16(centralHeader, 0); appendUint16(centralHeader, 0); appendUint32(centralHeader, 0); appendUint32(centralHeader, offset);
        const centralBytes = new Uint8Array(centralHeader);
        centralParts.push(centralBytes, name);
        centralSize += centralBytes.length + name.length;
        offset += localBytes.length + name.length + data.length;
      });
      const end:number[] = [];
      appendUint32(end, 0x06054b50); appendUint16(end, 0); appendUint16(end, 0); appendUint16(end, entries.length); appendUint16(end, entries.length); appendUint32(end, centralSize); appendUint32(end, offset); appendUint16(end, 0);
      return new Blob([...localParts, ...centralParts, new Uint8Array(end)], { type: mimeType });
    }

    export function xlsxFor(rows:Rows) {
      const sheetName = 'Data';
      return storedZip([
        { name: '[Content_Types].xml', data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>` },
        { name: '_rels/.rels', data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>` },
        { name: 'xl/workbook.xml', data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="${sheetName}" sheetId="1" r:id="rId1"/></sheets></workbook>` },
        { name: 'xl/_rels/workbook.xml.rels', data: `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/></Relationships>` },
        { name: 'xl/worksheets/sheet1.xml', data: worksheetXml(rows) }
      ], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
    }
