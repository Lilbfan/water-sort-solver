import globals from 'globals';
import pluginJs from '@eslint/js';
import tseslint from 'typescript-eslint';
import pluginVue from 'eslint-plugin-vue';

/** @type {import('eslint').Linter.Config[]} */
export default [
	{
		ignores: [
			'node_modules/',
			'dist/',
			'build/',
			'*.min.js',
			'src/generated/**', // Example of ignoring a specific directory
		],
	},
	{files: ['**/*.{js,mjs,cjs,ts,vue}']},
	{languageOptions: {globals: globals.browser}},
	pluginJs.configs.recommended,
	...tseslint.configs.recommended,
	...pluginVue.configs['flat/essential'],
	{
		files: ['**/*.vue'],
		languageOptions: {parserOptions: {parser: tseslint.parser}},
	},
];
