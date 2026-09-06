export function supportEtude(image: unknown): {fichier: string; alt: string; credit: string} | null {
  if (!image || typeof image !== 'object') return null;
  const i = image as Record<string, unknown>;
  if (typeof i.fichier !== 'string' || !/^images\/[a-zA-Z0-9_-]+\.(svg|png|jpg|jpeg|webp)$/.test(i.fichier)
    || typeof i.alt !== 'string' || !i.alt.trim() || typeof i.credit !== 'string' || !i.credit.trim()) return null;
  return {fichier: i.fichier, alt: i.alt, credit: i.credit};
}
