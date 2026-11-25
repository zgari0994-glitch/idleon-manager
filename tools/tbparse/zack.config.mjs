import base from '../../vitest.config.js';
export default { ...base, test: { globals: true, environment: 'node', include: ['tools/parse-golden/zack.test.mjs'], testTimeout: 600000 } };
