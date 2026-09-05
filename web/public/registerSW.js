if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    const base = location.pathname.startsWith('/academie-acces/') ? '/academie-acces/' : '/academie/';
    navigator.serviceWorker.register(base + 'sw.js', {scope:base, updateViaCache:'none'})
      .then(registration => {
        const verifie = () => { if (navigator.onLine) void registration.update().catch(() => {}); };
        window.addEventListener('online', verifie);
        document.addEventListener('visibilitychange', () => { if (!document.hidden) verifie(); });
      }).catch(() => {});
  });
}
