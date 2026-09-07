// Reprise depuis une page hors du scope des anciennes applications.
// Seuls les enregistrements de code sont remplacés ; aucune donnée n'est effacée.
document.getElementById('actualiser').addEventListener('click', async () => {
  const bouton = document.getElementById('actualiser');
  const etat = document.getElementById('etat');
  bouton.disabled = true;
  etat.textContent = 'Actualisation en cours…';
  try {
    if ('serviceWorker' in navigator) {
      const scopes = ['/academie/', '/academie-acces/'];
      const anciens = (await navigator.serviceWorker.getRegistrations()).filter(r => {
        const u = new URL(r.scope); return u.origin === location.origin && scopes.includes(u.pathname);
      });
      // Une ancienne installation peut échouer pendant son précache. Retirer
      // son enregistrement rend la prochaine navigation au réseau, sans toucher
      // aux caches, à IndexedDB, au localStorage ni au cookie de session.
      for (const r of anciens) await r.unregister();
    }
    etat.textContent = 'Application actualisée. Tes réponses sont conservées.';
    document.getElementById('ouvrir').hidden = false;
    location.replace('/academie/');
  } catch {
    etat.textContent = 'L’actualisation n’a pas abouti. Réessaie après avoir fermé les autres onglets Académie.';
    bouton.disabled = false;
  }
});
