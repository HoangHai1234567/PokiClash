import '@fontsource/baloo-2/700.css';
import '@fontsource/baloo-2/800.css';
import '@fontsource/pangolin/400.css';
import './view/style.css';
import { App, setApp } from './view/app';
import { battleScreen } from './view/battle/battleScreen';
import { cardsScreen } from './view/screens/cards';
import { heroesScreen } from './view/screens/heroes';
import { machineScreen } from './view/screens/machine';
import { openAfk } from './view/screens/map';
import { worldScreen } from './view/screens/world';
import { zoneScreen } from './view/screens/zone';
import { notebookScreen } from './view/screens/notebook';
import { bootVariant, runBoot } from './view/boot/boot';

const app = new App(document.getElementById('root')!);
setApp(app);
app.screens = {
  world: worldScreen,
  zone: zoneScreen,
  heroes: heroesScreen,
  cards: cardsScreen,
  machine: machineScreen,
  notebook: notebookScreen,
  battle: battleScreen,
};
app.openAfk = openAfk;

// ?screen=machine để mở thẳng một màn (dùng khi chụp màn hình kiểm tra)
const q = new URLSearchParams(location.search);
const start = q.get('screen') ?? 'world';
if (q.get('fresh') !== null) app.reset();
if (q.get('skipintro') !== null) app.save.intro = true;
// màn boot: mở game thẳng vào sảnh thì diễn trước (bỏ qua bằng ?skipboot hoặc ?skipintro; ?boot=a|b|c chọn ý tưởng, xem cả khi mở scene khác)
const wantBoot = q.get('boot') !== null || (start === 'world' && q.get('skipboot') === null && q.get('skipintro') === null);
if (wantBoot) app.booting = true;
if (start === 'battle') app.go('battle', { stageId: Number(q.get('stage') ?? 1), team: app.save.team }, false);
else if (start === 'zone') app.go('zone', { zone: q.get('zone') ?? 'thuy' }, false);
else app.go(start, undefined, false);
if (wantBoot) void runBoot(bootVariant(q)).then(() => app.endBoot());

// móc để thử nhanh trong console (chỉ bản dev)
if (import.meta.env.DEV) Object.assign(window as unknown as Record<string, unknown>, { pc: { app, CFG: (await import('./core/data/config')).CFG } });
