<script setup lang="ts">
import {ref} from 'vue';
import colorTube from './components/colorTube.vue';
import axios from 'axios';

interface step {
	from: number;
	to: number;
}

const COLORS: string[] = [
	'rgb(255, 0, 0)',
	'rgb(0, 255, 0)',
	'rgb(0, 0, 255)',
	'rgb(255, 192, 203)',
	'rgb(255, 255, 0)',
	'rgb(0, 255, 255)',
	'rgb(34, 139, 34)',
];
const tubes = ref<string[][]>([
	['rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)'],
	['rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)'],
	['rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)'],
	['rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)'],
	[],
	[],
]);

let solution = ref<step[] | null | undefined>(undefined);

// TODO: Reset tubes is not working, seems to be display error since the default tubes are not displayed either.
const buttons = [
	{title: 'add', text: 'Add a tube', action: () => tubes.value.push([])},
	{title: 'remove', text: 'Remove a tube', action: () => tubes.value.pop()},
	{
		title: 'reset',
		text: 'Reset all tubes',
		action: () => {
			tubes.value = [[]];
			solution.value = undefined;
		},
	},
	{
		title: 'solve',
		text: 'Solve problem',
		action: async () => {
			const tubes_copy = JSON.parse(JSON.stringify(tubes.value));
			try {
				// TODO: Mask the solution while waiting for the response
				const response = await axios.post('/api/solve', {
					tubes: tubes_copy,
				});
				solution.value = response.solution ? response.solution : null;
			} catch (error) {
				console.error(error);
			}
		},
	},
];
</script>

<template>
	<div>
		<h1>Water Sort Solver</h1>
		<div class="container-colors">
			<button
				v-for="(color, index) in COLORS"
				class="btn-color"
				:style="{backgroundColor: color}"
				:key="'color_' + index"
				@click="
					() => {
						if (tubes[tubes.length - 1].length < 4) {
							tubes[tubes.length - 1].push(color);
						}
					}
				"
			/>
		</div>
		<div class="container-tubes" :key="container - tubes">
			<colorTube
				v-for="(colors_in_tube, index) in tubes"
				:colors_in_tube="colors_in_tube"
				:key="'colors_in_tube_' + index"
			/>
		</div>
		<button
			class="button"
			v-for="button in buttons"
			:key="'button_' + button.title"
			@click="button.action"
		>
			{{ button.text }}
		</button>
		<div v-if="solution !== undefined">
			<h1>Solution</h1>
			<div v-if="solution">
				<div v-for="(step, index) in solution" :key="'step_' + index">
					<!-- TODO: Draw a fany UI to show the steps -->
					<p>Move from tube {{ step.from }} to tube {{ step.to }}</p>
				</div>
			</div>
			<div v-else>
				<h2>No solution found</h2>
			</div>
		</div>
	</div>
</template>

<style scoped>
.container-colors {
	height: 100px;
	display: flex;
	flex-direction: row;
	justify-content: center;

	.btn-color {
		width: 50px;
		height: 50px;
		margin: 10px;
	}
}

.container-tubes {
	display: flex;
	flex-direction: row;
	justify-content: center;
}

.button {
	margin: 10px;
}
</style>
