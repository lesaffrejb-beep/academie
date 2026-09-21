# demarrer.ps1 : le premier geste sur un Windows sans Python.
#
# Chantier ACA-DEMARRAGE-1. `app/demarrer.py` est le diagnostic complet,
# mais il ne peut pas tourner si Python manque : ce script est l'entree
# de secours. Il verifie Git et Python, propose les memes identifiants
# winget que le diagnostic, et ne telecharge jamais un executable pour
# le lancer ensuite.
#
#   powershell -ExecutionPolicy Bypass -File demarrer.ps1
#   powershell -ExecutionPolicy Bypass -File demarrer.ps1 -Installer
#   pwsh -NoProfile -File demarrer.ps1 -Diagnostic   (test CI)
#
# Les identifiants sont lus dans microsoft/winget-pkgs le 21/09/2026 :
#   Git.Git                 (installeur Scope: user)
#   Python.Python.3.12      (installeur Scope: user)
# `--scope user` installe pour l'utilisateur courant, sans elever les
# droits. Aucune elevation automatique, aucun telechargement manuel.

[CmdletBinding()]
param(
    [switch]$Installer,
    [switch]$Diagnostic,
    [string[]]$CandidatPython = @()
)

$ErrorActionPreference = "Stop"

# Les candidats Windows : `py -3` (lanceur officiel, souvent installe
# avant que `python` n'apparaisse), puis `python3`, puis `python`. Un
# alias Microsoft Store qui echoue ne doit pas faire croire a un Python
# pret : chaque candidat est interroge pour de vrai.
#
# Pas de virgule unaire devant le tableau ici : elle fait sortir UN
# objet du pipeline, et l'appel en boucle recoit alors une seule chaine
# « py -3 python3 python » a la place des trois candidats. Tous les
# candidats echouaient, et un poste pourvu de Python etait declare
# « absent ou inutilisable » (CI Windows du 21/09/2026). Les appelants
# garantissent le tableau avec @(...).
function Get-CandidatsPython {
    if ($CandidatPython.Count -gt 0) { return $CandidatPython }
    return @("py -3", "python3", "python")
}

# Un candidat se lit en deux morceaux : le nom du lanceur et ses
# arguments propres (`py` + `-3`). Les garder ensemble dans une chaine
# faisait perdre le `-3` au moment d'appeler le diagnostic complet.
function Split-Candidat {
    param([string]$Candidat)
    $morceaux = @($Candidat -split "\s+" | Where-Object { $_ -ne "" })
    $prefixes = @()
    if ($morceaux.Count -gt 1) {
        $prefixes = @($morceaux[1..($morceaux.Count - 1)])
    }
    return [pscustomobject]@{ Nom = $morceaux[0]; Prefixes = $prefixes }
}

function Invoque-PythonCandidat {
    param([string]$Candidat, [string[]]$Arguments)
    $parties = Split-Candidat -Candidat $Candidat
    $nom = $parties.Nom
    $reste = @($parties.Prefixes)
    $exe = Get-Command $nom -ErrorAction SilentlyContinue
    if (-not $exe) { return $null }
    try {
        # `-X utf8` force la sortie UTF-8 : sinon un cp1252 casse les
        # accents du diagnostic.
        $sortie = & $nom @reste "-X" "utf8" @Arguments 2>&1
        $code = $LASTEXITCODE
    } catch {
        return $null
    }
    if ($null -eq $code -or $code -ne 0) { return $null }
    return ($sortie | Out-String).Trim()
}

# Le Python utilisable du poste, ou $null. On garde son nom : le
# diagnostic le transmet ensuite pour ne pas relancer un candidat muet.
function Resolve-PythonPret {
    foreach ($candidat in @(Get-CandidatsPython)) {
        $sortie = Invoque-PythonCandidat -Candidat $candidat `
            -Arguments @("-c", "import sys; print('%d.%d' % sys.version_info[:2])")
        if (-not $sortie) { continue }
        if ($sortie -notmatch "(\d+)\.(\d+)") { continue }
        $majeur = [int]$Matches[1]
        $mineur = [int]$Matches[2]
        if ($majeur -gt 3 -or ($majeur -eq 3 -and $mineur -ge 12)) {
            return $candidat
        }
    }
    return $null
}

function Test-GitPret {
    $git = Get-Command git -ErrorAction SilentlyContinue
    if (-not $git) { return $false }
    try {
        $sortie = (& git --version 2>&1 | Out-String)
    } catch {
        return $false
    }
    if ($LASTEXITCODE -ne 0) { return $false }
    return ($sortie -match "\d+\.\d+\.\d+")
}

function Test-Winget {
    return [bool](Get-Command winget -ErrorAction SilentlyContinue)
}

function Show-Installation {
    Write-Host "winget install --id Git.Git --scope user --source winget --accept-package-agreements --accept-source-agreements"
    Write-Host "winget install --id Python.Python.3.12 --scope user --source winget --accept-package-agreements --accept-source-agreements"
}

# winget sort un code : un echec ne doit jamais finir en message de
# succes. La sortie native part vers l'ecran, puis on capture le code
# dans une variable avant de la rendre : sans le `Out-Host`, la sortie
# texte et le nombre remontent melanges dans le pipeline et la
# comparaison a zero devient fausse.
function Install-AvecWinget {
    param([string]$Piece)
    & winget install --id $Piece --scope user --source winget `
        --accept-package-agreements --accept-source-agreements 2>&1 | Out-Host
    $code = $LASTEXITCODE
    if ($null -eq $code) { return 1 }
    return [int]$code
}

$gitPret = Test-GitPret
$pythonPret = Resolve-PythonPret

if ($gitPret) { Write-Host "Git : present et utilisable" } else { Write-Host "Git : absent ou sans reponse" }
if ($pythonPret) { Write-Host "Python 3.12 ou plus recent : present ($pythonPret)" }
else { Write-Host "Python 3.12 ou plus recent : absent ou inutilisable" }
Write-Host "Etat local : etat/ (hors git, non synchronise entre machines)"
Write-Host "  sauvegarde : python app/academie.py exporter <fichier>"
Write-Host "  reprise   : python app/academie.py importer <fichier>"

# Le diagnostic complet et le hook vivent dans le Python du depot. On
# reutilise le candidat resolu, arguments compris (`py -3`), et on lit
# son code de sortie : un diagnostic muet ne doit pas passer pour vert.
# `$codeDiagnostic` reste `$null` quand le diagnostic n'a pas tourne ;
# `$diagnosticAbsent` distingue ce cas d'un echec (code non nul).
$codeDiagnostic = $null
$diagnosticAbsent = $false
if ($pythonPret) {
    if (Test-Path "app/demarrer.py") {
        Write-Host "Diagnostic complet :"
        $parties = Split-Candidat -Candidat $pythonPret
        $prefixes = @($parties.Prefixes)
        & $parties.Nom @prefixes "-X" "utf8" "app/demarrer.py" "--json"
        $codeDiagnostic = $LASTEXITCODE
    } else {
        $diagnosticAbsent = $true
        Write-Host "app/demarrer.py introuvable : ce dossier n'est pas la racine du depot."
    }
}

if ($Diagnostic) {
    # Mode CI : on rapporte l'etat, on n'installe rien.
    if (-not $gitPret -or -not $pythonPret) { exit 1 }
    if ($diagnosticAbsent) {
        Write-Host "Diagnostic incomplet : app/demarrer.py est absent, ce dossier n'est pas la racine du depot."
        exit 1
    }
    if ($null -eq $codeDiagnostic) {
        Write-Host "Diagnostic incomplet : il n'a pas pu etre execute."
        exit 1
    }
    if ($codeDiagnostic -ne 0) { exit 1 }
    exit 0
}

if ($gitPret -and $pythonPret) {
    if ($diagnosticAbsent) {
        Write-Host "Diagnostic incomplet : app/demarrer.py est absent, ce dossier n'est pas la racine du depot."
        exit 1
    }
    if ($null -eq $codeDiagnostic) {
        Write-Host "Diagnostic incomplet : il n'a pas pu etre execute."
        exit 1
    }
    if ($codeDiagnostic -ne 0) {
        Write-Host "Le diagnostic complet a signale un probleme : lire sa sortie ci-dessus."
        exit 1
    }
    Write-Host "Outils prets. Le profil, le cursus et le hook sont lus ci-dessus par app/demarrer.py."
    exit 0
}

if (-not (Test-Winget)) {
    Write-Host "winget est absent : installer Git et Python 3.12 depuis les sources officielles, puis relancer."
    Show-Installation
    exit 1
}

if (-not $Installer) {
    Write-Host "A faire : installer les outils manquants avec winget."
    Show-Installation
    Write-Host "Relancer avec -Installer pour executer ces commandes."
    exit 0
}

$echecs = @()
if (-not $gitPret) {
    $code = Install-AvecWinget -Piece "Git.Git"
    if ($code -ne 0) { $echecs += "Git.Git (code $code)" }
}
if (-not $pythonPret) {
    $code = Install-AvecWinget -Piece "Python.Python.3.12"
    if ($code -ne 0) { $echecs += "Python.Python.3.12 (code $code)" }
}

if ($echecs.Count -gt 0) {
    Write-Host "Installation en echec : $($echecs -join ', ')"
    exit 1
}

# On re-teste pour de vrai : le PATH de la session courante peut ne pas
# voir l'installation, et un code 0 de winget ne prouve rien seul.
$gitApres = Test-GitPret
$pythonApres = Resolve-PythonPret
if (-not $gitApres -or -not $pythonApres) {
    Write-Host "Installation lancee, mais ce terminal ne voit pas encore les outils."
    Write-Host "Fermer et rouvrir le terminal, puis relancer : python app/demarrer.py --json"
    exit 1
}

# Le hook et le profil ne sont pas poses par winget : on relance le
# diagnostic complet pour ne pas annoncer un poste pret a tort.
if (-not (Test-Path "app/demarrer.py")) {
    Write-Host "Diagnostic incomplet : app/demarrer.py est absent, ce dossier n'est pas la racine du depot."
    exit 1
}
Write-Host "Diagnostic complet :"
$parties = Split-Candidat -Candidat $pythonApres
$prefixes = @($parties.Prefixes)
& $parties.Nom @prefixes "-X" "utf8" "app/demarrer.py" "--json"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Le diagnostic complet a signale un probleme apres installation : lire sa sortie ci-dessus."
    exit 1
}

Write-Host "Outils installes et verifies. Prochain geste : relancer app/demarrer.py et suivre ce qu'il reste a faire."
exit 0
