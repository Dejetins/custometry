export function pilotPeriod(period:{grain:string;value:string}):{start:string;end:string}{
 const year=Number(period.value.slice(0,4));const iso=(date:Date)=>date.toISOString().slice(0,10);
 if(period.grain==='day')return {start:period.value,end:period.value};
 if(period.grain==='week'){
  const week=Number(period.value.split('-W')[1]);const fourth=new Date(Date.UTC(year,0,4));const monday=new Date(Date.UTC(year,0,4-((fourth.getUTCDay()+6)%7)+(week-1)*7));
  return {start:iso(monday),end:iso(new Date(monday.getTime()+6*86400000))};
 }
 const month=period.grain==='month'?Number(period.value.slice(5,7))-1:period.grain==='quarter'?(Number(period.value.slice(-1))-1)*3:0;
 const length=period.grain==='month'?1:period.grain==='quarter'?3:12;
 return {start:iso(new Date(Date.UTC(year,month,1))),end:iso(new Date(Date.UTC(year,month+length,0)))};
}
