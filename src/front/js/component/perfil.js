import { useEffect, useContext } from "react";
import React from "react";
import { Context } from "../store/appContext";

export const Perfil = () => {
  const { store, actions } = useContext(Context);
  useEffect(() => {
    actions.privado();
  }, []);
  return (
    <h1>
      {store.permiso
        ? `Acceso a espacio privado permitido ${store.user}`
        : "404 la pagina no existe"}
    </h1>
  );
};
