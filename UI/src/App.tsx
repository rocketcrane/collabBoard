import { memo } from 'react';
import type { FC } from 'react';

import classes from './App.module.css';
import resets from './components/_resets.module.css';
import { Frame250 } from './components/Frame250/Frame250.js';

import { JSONData } from './types';
import data from '../public/data_new.json';

interface Props {
  className?: string;
}
export const App: FC<Props> = memo(function App(props = {}) {
  return (
    <div className={`${resets.clapyResets} ${classes.root}`}>
      <Frame250 data={data}/>
    </div>
  );
});
