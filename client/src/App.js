import { createContext } from 'react';

import Home from "./pages/Home";
import "./style.scss"

const EnvContext = createContext({})

function App() {
  return (
    <EnvContext.Provider value={process.env}>
      <Home/>
    </EnvContext.Provider>
  );
}

export default {App, EnvContext};
