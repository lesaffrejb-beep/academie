import { defineConfig } from "vitest/config";

/**
 * Les tests tournent sans le plugin PWA ni React : ils jugent le moteur
 * et le depot, pas le rendu. La couche visuelle ajoutera sa propre
 * configuration jsdom quand elle aura des composants a monter.
 */
export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    include: ["src/**/*.test.ts", "tests/**/*.test.ts"],
    exclude: ["node_modules/**", "dist/**", "tests/e2e/**"],
    // parite.test.ts lance python3 : la premiere execution peut trainer.
    testTimeout: 60000,
  },
});
