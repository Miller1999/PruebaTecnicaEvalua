<template>
	<div>
		<img
			src="https://cdn.dribbble.com/users/1022481/screenshots/3018253/404-snow.gif"
			alt="Not found"
		/>
		<router-link to="/"
			><button>{{ $t("inventory.returnToProducts") }}</button></router-link
		>
	</div>
</template>

<script>
export default {
	name: "NotFound",
};
</script>

<style lang="scss" scoped>
div {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	width: 100%;
	img {
		max-width: 500px;
		width: 100%;
	}
	button {
		margin-top: 1rem;
		padding: 0.5rem;
		border: 1px solid #ccc;
		border-radius: 5px;
	}
}
</style>
