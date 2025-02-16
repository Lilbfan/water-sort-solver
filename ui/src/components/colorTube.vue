// Component: colorTube
<script setup lang="ts">
	import { ref, watch } from 'vue'
	import _ from 'lodash'
	
	const props = defineProps<{ colors_in_tube: string[] }>()
	const EMPTY_COLOR = 'rgb(64, 64, 64)'

	let upper_color = ref(Array(3).fill(EMPTY_COLOR))
	let bottom_color = ref(EMPTY_COLOR)

	watch(props.colors_in_tube, () => {
		let colors_in_tube = _.cloneDeep(props.colors_in_tube).reverse() as string[]
		while (colors_in_tube.length < 4) {
			colors_in_tube.unshift(EMPTY_COLOR)
		}
		upper_color.value = colors_in_tube.slice(0, colors_in_tube.length - 1)
		bottom_color.value = colors_in_tube[colors_in_tube.length - 1]
	})
</script>

<template>
	<div class="color-tube">
		<div v-for="color, index in upper_color" class="color-layer" :style="{ backgroundColor: color }" :key="'color_' + index" />
		<div class="color-layer-bottom" :style="{ backgroundColor: bottom_color }" />
	</div>
</template>

<style scoped>
.color-tube {
	display: flex;
	margin: 20px;
	flex-direction: column;
	align-items: center;
	width: 100px;
	height: 400px;

	.color-layer {
		width: 100%;
		height: 100px;
		border-style: solid;
		border-bottom-style: none;
	}

	.color-layer-bottom {
		width: 100%;
		height: 100px;
		border-style: solid;
		border-radius: 0 0 30% 30%;
	}
}
</style>
