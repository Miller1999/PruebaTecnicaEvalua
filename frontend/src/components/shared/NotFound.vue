<template>
	<div>
		<!-- Imagen que se muestra cuando no se encuentra la página -->

		<img src="../../assets/404NotFound.png" alt="Not found" />
		<!-- Botón que redirige a la página principal de productos -->

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
	margin-top: 5rem;
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
