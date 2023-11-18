import {readFile} from 'node:fs/promises';

export default async (g: string, c: string, ocwd: string) => {
  try {
    return await readFile(`${process.cwd()}/tests/pyanalyzer/${g}/${c}/_${c}-report-pyanalyzer.json`, 'utf-8');
  } catch (e: any) {
    console.error(e);
    return false;
  }
};
