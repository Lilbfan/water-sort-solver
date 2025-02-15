<script setup lang="ts">
import { ref } from 'vue'
import Tube from './components/Tube.vue'

const colors: string[] = [
	'rgb(255, 0, 0)',
	'rgb(0, 255, 0)',
	'rgb(0, 0, 255)',
	'rgb(255, 192, 203)',
	'rgb(255, 255, 0)',
	'rgb(0, 255, 255)',
	'rgb(34, 139, 34)',
]
const tubes = ref<string[][]>([[]])

const buttons = [
	{ text: 'Add a tube', action: () => tubes.value.push([]) },
	{ text: 'Remove last tube', action: () => tubes.value.pop() },
	{ text: 'Reset all tubes', action: () => tubes.value = [[]] },
	{ text: 'Solve problem', action: async () => {
		const tubes_copy = JSON.parse(JSON.stringify(tubes.value))
		let url = new URL(window.location.href)
		url.pathname = url.pathname + 'solve'
		try {
			const response = await fetch(url.href, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ tubes: tubes_copy }),
			})
			console.log(response)
		} catch (error) {
			console.error(error)
		}
	} },
]

</script>

<template>
	<div>
		<h1>Water Sort Solver</h1>
		<div class="container-colors" >
			<button
				v-for="color in colors"
				class="btn-color"
				:style="{ backgroundColor: color }"
				@click="() => {
					if (tubes[tubes.length - 1].length < 4) {
						tubes[tubes.length - 1].push(color)
					}
				}"
			/>
		</div>
		<div class="container-tubes">
			<Tube
				v-for="colors_in_tube in tubes"
				:colors_in_tube="colors_in_tube"
			/>
		</div>
		<button
			class="button"
			v-for="button in buttons"
			@click="button.action"
		>
			{{ button.text }}
		</button>
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
