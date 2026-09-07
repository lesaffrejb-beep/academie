import {defineConfig} from "@playwright/test";
export default defineConfig({
  expect:{timeout:15000},
  testDir:"./tests/onboarding", workers:1, timeout:60000,
  use:{baseURL:"http://127.0.0.1:5197/academie/",viewport:{width:375,height:812},launchOptions:{executablePath:process.env.CHROMIUM_PATH}},
  webServer:{command:"python3 ../serveur/essai_local.py --port 5197 --base ../etat/tests-onboarding.sqlite",url:"http://127.0.0.1:5197/academie/",reuseExistingServer:false},
});
