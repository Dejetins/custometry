import {describe,it,expect} from 'vitest';
import {resolveApplicationRoute} from '../../app/router/route-resolution';
describe('composer route negotiation',()=>{
 it('admits the explicit composer editor and exact preview',()=>{
  expect(resolveApplicationRoute('/w/test/reports/new/edit','?view=composer').kind).toBe('route');
  expect(resolveApplicationRoute('/w/test/reports/report/snapshots/snapshot','?view=composer').kind).toBe('route');
 });
 it('keeps unknown query parameters and unrelated routes closed',()=>{
  expect(resolveApplicationRoute('/w/test/reports/new/edit','?unknown=1').kind).toBe('system');
  expect(resolveApplicationRoute('/auth/sign-in','?view=composer').kind).toBe('system');
 });
});
