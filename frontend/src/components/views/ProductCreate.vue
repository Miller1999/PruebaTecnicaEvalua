<template>
	<div v-if="isVisible" class="modal">
		<div class="modal-content">
			<header class="modal-header">
				<h3>{{ title }}</h3>
				<button @click="closeModal">&times;</button>
			</header>
			<div class="modal-body">
				<slot></slot>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: "ProductCreate",
	props: {
		title: {
			type: String,
			required: true,
		},
		isVisible: {
			type: Boolean,
			default: false,
		},
		isEditing: {
			type: Boolean,
			default: false,
		},
	},
	methods: {
		closeModal() {
			this.$emit("close");
			this.$emit("closeEdit");
		},
	},
};
</script>

<style lang="scss" scoped>
@import "../../stylessheets/helpers/variables";
.modal {
	position: fixed;
	z-index: 10;
	left: 0;
	top: 0;
	width: 100%;
	height: 100%;
	overflow: auto;
	background-color: rgba(0, 0, 0, 0.5);
	display: flex;
	justify-content: center;
	align-items: center;
	.modal-content {
		width: 90%;
		max-width: 800px;
		background-color: #fff;
		padding: 1rem;
		border-radius: 5px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
		.modal-header {
			display: flex;
			justify-content: space-between;
			align-items: center;
			h3 {
				font-size: 1rem;
				font-weight: 900;
			}
			button {
				border: none;
				background-color: transparent;
				font-size: 2rem;
				color: #000;
			}
		}

		form {
			display: flex;
			flex-direction: column;
			text-align: left;
			gap: 1rem;
			.form-group {
				display: flex;
				gap: 0.5rem;
				label {
					font-weight: bold;
				}
			}
			input {
				padding: 0.5rem;
				border: 1px solid #ccc;
				border-radius: 5px;
				font-size: 1rem;
			}
			button {
				padding: 0.5rem;
				border: 1px solid #ccc;
				border-radius: 5px;
				font-size: 1rem;
				background-color: $ColorVueBg;
				color: black;
			}
		}
	}
}
</style>
