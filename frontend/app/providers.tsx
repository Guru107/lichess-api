"use client";

import * as React from "react";
import { NextUIProvider } from "@nextui-org/system";
import { useRouter } from "next/navigation";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import { ThemeProviderProps } from "next-themes/dist/types";

export interface ProvidersProps {
  children: React.ReactNode;
  themeProps?: ThemeProviderProps;
}

interface Action {
  type: String
}

const StateContext = React.createContext({})

export function useStateContext() {
  return React.useContext(StateContext)
}
function reducer(state, action: Action) {

  throw Error('Unknown action: ' + action.type); 
}

function createInitialState() {
  return {}
}
export function Providers({ children, themeProps }: ProvidersProps) {
  const router = useRouter();

  const [apiState, dispatch] = React.useReducer(reducer, null, createInitialState)

  return (
    <NextUIProvider navigate={router.push}>
      <NextThemesProvider {...themeProps}>
        <StateContext.Provider value={[apiState, dispatch]}>
          {children}
        </StateContext.Provider>
      </NextThemesProvider>
    </NextUIProvider>
  );
}


