import {cleanup,fireEvent,render,screen} from '@testing-library/react';
import {afterEach,expect,it,vi} from 'vitest';
import {ReportComparisonControl} from './ReportComparisonControl';
afterEach(cleanup);
it('clears delta display when temporal comparison is removed, retaining the card identity',()=>{
 const change=vi.fn();render(<ReportComparisonControl selection={{mode:'single',card_id:'revenue',temporal:'previous_year_same_dates',display:'delta_trend'}} disabled={false} locale="en" none="None" prior="Same dates last year" onChange={change}/>);
 fireEvent.change(screen.getByRole('combobox',{name:'Card comparison'}),{target:{value:'none'}});
 expect(change).toHaveBeenCalledWith({mode:'single',card_id:'revenue',temporal:'none',display:'series'});
});
it('preserves the existing series choice when temporal comparison is enabled',()=>{
 const change=vi.fn();render(<ReportComparisonControl selection={{mode:'single',card_id:'receipts',temporal:'none',display:'series'}} disabled={false} locale="ru" none="Нет" prior="Год назад" onChange={change}/>);
 fireEvent.change(screen.getByRole('combobox',{name:'Сравнение карточки'}),{target:{value:'previous_year_same_dates'}});
 expect(change).toHaveBeenCalledWith({mode:'single',card_id:'receipts',temporal:'previous_year_same_dates',display:'series'});
});
