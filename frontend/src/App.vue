<template>
	<div id="app">
		<nav id="nav">
			<img alt="Vue logo" src="@/assets/logo.png" />
			<router-link to="/">{{ $t("inventory.products") }}</router-link>
			<ThemeToggler />
		</nav>
		<router-view />
	</div>
</template>
<script>
import ThemeToggler from "./components/shared/ThemeToggler.vue";

export default {
	components: {
		ThemeToggler,
	},
};
</script>
<style lang="scss">
@import "bootstrap-icons/font/bootstrap-icons.css";
@import "./stylessheets/helpers/variables";
#app {
	font-family: Avenir, Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	text-align: center;
	color: #2c3e50;
	display: flex;
	flex-direction: column;
	align-items: center;
}

#nav {
	display: flex;
	justify-content: space-around;
	align-items: center;
	width: 80%;
	padding: 1rem;
	img {
		height: 50px;
	}
	a {
		font-weight: bold;
		color: #2c3e50;

		&.router-link-exact-active {
			color: #42b983;
		}
	}
	@media (max-width: 767px) {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		z-index: 10;
		width: 100%;
	}
}
</style>
