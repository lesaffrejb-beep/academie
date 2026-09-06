import { describe, it, expect } from "vitest";
import { nomJournal, clePrivee, valideCompte } from "./compte";
import { ligneValide } from "../donnees/api";

describe("compte et sauvegarde", () => {
  it("sépare les bases et les brouillons sans adopter l'ancien journal", () => {
    expect(nomJournal("alice")).not.toBe(nomJournal("bob"));
    expect(nomJournal("alice")).not.toBe("academie-journal");
    expect(clePrivee("brouillon", "alice")).not.toBe(clePrivee("brouillon", "bob"));
  });
  it("refuse pseudo vide et phrase secrète courte", () => {
    expect(valideCompte("abcdefghijklm", " ")).toBeTruthy();
    expect(valideCompte("court", "A")).toBeTruthy();
    expect(valideCompte("abcdefghijklm", "A")).toBe("");
  });
  it("accepte uniquement un événement de cursus bien formé", () => {
    const l = {quand:"2026-09-05T12:00:00Z", nonce:"abcdefgh", mode:"cursus"};
    expect(ligneValide(l)).toBe(false);
    expect(ligneValide({...l,cursus:123})).toBe(false);
    expect(ligneValide({...l,cursus:"ifsi"})).toBe(true);
  });
});
