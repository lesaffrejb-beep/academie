import {useState} from 'react';
import {supportEtude} from './validationSupport';

export function SupportEtude({image, onCharge}: {image: unknown; onCharge: (ok: boolean) => void}) {
  const support = supportEtude(image);
  const [erreur, setErreur] = useState(false);
  const [agrandi, setAgrandi] = useState(false);
  if (!support || erreur) return <p role="alert">Le support ne peut pas être chargé. Réessaie plus tard ; aucune réponse ne sera créditée.</p>;
  return <figure className="etude-support">
    <div className="etude-support-cadre" tabIndex={agrandi ? 0 : undefined} aria-label={agrandi ? 'Support agrandi, défilement horizontal' : undefined}>
      <img style={agrandi ? {width: '200%', maxWidth: 'none', minWidth: 700} : undefined} src={`/academie/${support.fichier}`} alt={support.alt}
        onLoad={() => onCharge(true)} onError={() => {setErreur(true); onCharge(false);}} />
    </div>
    <figcaption>{support.credit}</figcaption>
    <button className="lien-action" type="button" aria-pressed={agrandi} onClick={() => setAgrandi(!agrandi)}>{agrandi ? 'Réduire le support' : 'Agrandir le support'}</button>
  </figure>;
}
