<template>
	<div id="app">
		<nav id="nav">
			<img alt="Vue logo" src="@/assets/logo.png" />
			<router-link to="/">{{ $t("inventory.products") }}</router-link>
			<button>Tema</button>
		</nav>
		<router-view />
	</div>
</template>

<style lang="scss">
#app {
	font-family: Avenir, Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	text-align: center;
	color: #2c3e50;
}

#nav {
	display: flex;
	justify-content: center;
	align-items: center;
	gap: 1rem;
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
}
</style>
