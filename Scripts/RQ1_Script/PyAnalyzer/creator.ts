import exec from '../../../common/exec';
import {mkdir} from 'fs/promises';

export default async (g: string, c: string, exepath: string) => {
  const ocwd = process.cwd();
  await mkdir(ocwd + `/tests/pyanalyzer/${g}/${c}`, {recursive: true});
  process.chdir(ocwd + `/tests/pyanalyzer/${g}/${c}`);
  try {
    await exec(`${exepath} ${ocwd}/tests/cases/_${g}/_${c}`);
  } catch {
    return false;
  } finally {
    process.chdir(ocwd);
  }

  return true;
};
