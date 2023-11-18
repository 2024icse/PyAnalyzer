import creator from './creator';
import extractor from './extractor';
import builder from './builder';
import {error} from '@pyanalyzer/logging';
import {CaseContainer} from '@pyanalyzer/doc-parser';
import {UNIMatcher} from '../../../matchers';
import {readFile} from 'node:fs/promises';

export default async (g: string, c: string, cs: CaseContainer, ocwd: string, exepath: string) => {
  try {
    const data = await readFile(`tests/sourcetrail/${g}/${c}.json`, 'utf-8');
    //console.log(data.replaceAll(/\s+/g, ' '));
    try {
      builder(data);
    } catch (e) {
      console.log(e);
    }
    return UNIMatcher(cs, 'python', 's');
  } catch {
    console.log('Running SourceTrail in background, please wait');
    if (await creator(g, c, exepath, ocwd)) {
      const data = await extractor(g, c, ocwd);
      if (data) {
        //console.log(data.replaceAll(/\s+/g, ' '));
        builder(data);
        return UNIMatcher(cs, 'python', 's');
      } else {
        error(`Failed to read sourcetrail output on ${g}/${c}`);
      }
    } else {
      error(`Failed to execute sourcetrail on ${g}/${c}`);
    }
  }
};
