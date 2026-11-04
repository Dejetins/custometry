import {composerReports as C} from '@custometry/contracts';
import {protectedFetch} from './report-api';
export const composerApi=new C.ComposerClient('/api/reports',protectedFetch);
