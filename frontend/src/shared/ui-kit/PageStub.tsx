/** Marcador de pantalla pendiente. Borrar cuando la feature tenga su pantalla real. */
export function PageStub({ title, owner }: { title: string; owner: string }) {
  return (
    <section className="rounded-lg border border-dashed border-slate-300 p-6">
      <h1 className="text-xl font-semibold text-slate-800">{title}</h1>
      <p className="mt-2 text-sm text-slate-500">Pantalla pendiente. Responsable: {owner}.</p>
    </section>
  );
}
