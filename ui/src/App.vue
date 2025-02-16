<script setup lang="ts">
import {ref, watch} from 'vue';
import colorTube from './components/colorTube.vue';
import axios from 'axios';

interface step {
	from: number;
	to: number;
	tubes: string[][];
}

const COLORS: string[] = [
	'rgb(255, 0, 0)',
	'rgb(255, 192, 203)',
	'rgb(255, 255, 0)',
	'rgb(0, 255, 0)',
	'rgb(34, 139, 34)',
	'rgb(0, 0, 255)',
	'rgb(0, 192, 255)',
	'rgb(0, 255, 255)',
];

const tubes = ref<string[][]>([
	// TODO: Just debugging use, delete this after testing
	['rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)'],
	['rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)'],
	['rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)'],
	['rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)'],
	[],
	[],
]);
const solution = ref<step[] | null | undefined>(undefined);
const isLoading = ref(false);
const colors_tube_key = ref(0);
const buttons = [
	{title: 'add', text: 'Add a tube', action: () => tubes.value.push([])},
	{
		title: 'remove',
		text: 'Remove a tube',
		action: () => {
			if (tubes.value.length > 1) {
				tubes.value.pop();
			}

			if (tubes.value.length === 1) {
				tubes.value = [];
			}
		},
	},
	{
		title: 'reset',
		text: 'Reset all tubes',
		action: () => {
			tubes.value = [];
			solution.value = undefined;
		},
	},
	{
		title: 'solve',
		text: 'Solve problem',
		action: async () => {
			const tubes_copy = JSON.parse(JSON.stringify(tubes.value));
			solution.value = undefined;
			isLoading.value = true;
			try {
				const response = await axios.post('/api/solve', {
					tubes: tubes_copy,
				});
				solution.value = response.data.solution
					? response.data.solution
					: null;
			} catch (error) {
				console.error(error);
			} finally {
				isLoading.value = false;
			}
		},
	},
];

watch(tubes, new_tubes => {
	if (new_tubes.length === 0) {
		tubes.value.push([]);
	}
	colors_tube_key.value += 1;
});
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
		<div class="container-tubes">
			<colorTube
				v-for="colors_in_tube in tubes"
				:colors_in_tube="colors_in_tube"
				:key="colors_tube_key"
				tube_style="unrelated"
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
				<div
					v-for="(step, index) in solution"
					:key="'step_' + index"
					class="container-step"
				>
					<h2>
						Move from tube {{ step.from }} to tube {{ step.to }}
					</h2>
					<div class="container-tubes">
						<colorTube
							v-for="(tube, index) in step.tubes"
							:colors_in_tube="tube"
							:key="'colors_tube_' + index"
							:tube_style="
								step.from === index
									? 'from'
									: step.to === index
										? 'to'
										: 'unrelated'
							"
						/>
					</div>
				</div>
			</div>
			<div v-else>
				<h2>No solution found</h2>
			</div>
		</div>
		<div v-else-if="isLoading" class="container-loading">
			<h1>Computing solution ...</h1>
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

.container-loading {
	margin: 200px 0px;
}

.container-step {
	margin-bottom: 320px;
}

.button {
	margin: 10px;
}
</style>
