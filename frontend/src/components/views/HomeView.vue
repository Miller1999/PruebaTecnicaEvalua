<template>
	<div class="home">
		<div class="nav">
			<div class="buttons">
				<button>
					<span>Filtrar</span>
					<ion-icon name="funnel-outline"></ion-icon>
				</button>
				<button>
					<span>Añadir Producto</span>
					<ion-icon name="add-outline"></ion-icon>
				</button>
			</div>
		</div>
		<!-- large screens -->
		<table v-if="isLargeScreen" class="table">
			<thead>
				<tr>
					<th scope="col">{{ $t("inventory.name") }}</th>
					<th scope="col">{{ $t("inventory.quantity") }}</th>
					<th scope="col">{{ $t("inventory.price") }}</th>
					<th scope="col">{{ $t("inventory.supplier") }}</th>
					<th scope="col">{{ $t("inventory.action") }}</th>
				</tr>
			</thead>
			<tbody>
				<tr scope="row" v-for="(product, index) in products" :key="index">
					<td>{{ product.name }}</td>
					<td>{{ product.quantity }}</td>
					<td>{{ product.price }}</td>
					<td>{{ product.supplier }}</td>
					<td>
						<b-button
							@click="
								$router.push({
									name: 'product',
									params: { idProduct: product.id_product },
								})
							"
						>
							<ion-icon name="create-outline"></ion-icon>
						</b-button>
						<b-button
							@click="deleteProduct(product.id_product)"
							variant="secondary"
						>
							<ion-icon name="trash-outline"></ion-icon>
						</b-button>
					</td>
				</tr>
			</tbody>
		</table>
		<!-- small screens -->
		<section v-else class="card__container">
			<article v-for="(product, index) in products" :key="index" class="card">
				<h2>{{ $t("inventory.name") }}: {{ product.name }}</h2>
				<p>
					<span>{{ $t("inventory.quantity") }}:</span> {{ product.quantity }}
				</p>
				<p>
					<span>{{ $t("inventory.price") }}:</span> {{ product.price }}
				</p>
				<p>
					<span>{{ $t("inventory.supplier") }}:</span> {{ product.supplier }}
				</p>
				<div class="card__actions">
					<b-button
						@click="
							$router.push({
								name: 'product',
								params: { idProduct: product.id_product },
							})
						"
					>
						<ion-icon name="create-outline"></ion-icon>
					</b-button>
					<b-button @click="deleteProduct(product.id_product)">
						<ion-icon name="trash-outline"></ion-icon>
					</b-button>
				</div>
			</article>
		</section>
	</div>
</template>

<script>
import VAPI from "@/http_common";
import { HTTP_STATUS, SERVICE_NAMES } from "@/app_constants";
export default {
	name: "HomeView",
	data() {
		return {
			products: [
				{
					id_product: 1,
					name: "Product 1",
					quantity: 10,
					price: 10,
					supplier: "Supplier 1",
				},
				{
					id_product: 2,
					name: "Product 2",
					quantity: 20,
					price: 20,
					supplier: "Supplier 2",
				},
				{
					id_product: 1,
					name: "Product 1",
					quantity: 10,
					price: 10,
					supplier: "Supplier 1",
				},
				{
					id_product: 2,
					name: "Product 2",
					quantity: 20,
					price: 20,
					supplier: "Supplier 2",
				},
			],
			isLargeScreen: true,
		};
	},
	mounted() {
		this.getAllProducts();
		this.checkScreenSize();
		window.addEventListener("resize", this.checkScreenSize);
	},
	methods: {
		checkScreenSize() {
			// Establece si la pantalla es grande o pequeña
			this.isLargeScreen = window.innerWidth > 767;
		},
		async getAllProducts() {
			try {
				let response = await VAPI.get(`${SERVICE_NAMES.INVENTORY}/get-all`);
				if (response.status == HTTP_STATUS.OK) {
					this.products = response.data;
				}
			} catch (error) {
				console.error(error);
			}
		},
		deleteProduct(idProduct) {
			console.log(idProduct);
			// TODO
		},
	},
};
</script>

<style lang="scss" scoped>
@import "../../stylessheets/helpers/variables";
/* Large screens */
.home {
	display: flex;
	flex-direction: column;
	align-items: center;
}
table {
	width: 90%;
	max-width: 1200px;
	margin: 1rem 0;
	border-collapse: collapse;
	border-spacing: 0;
	font-size: 1rem;
	thead {
		th {
			text-align: center;
			padding: 0.5rem;
			background-color: $ColorBodyBg;
		}
	}
	tbody {
		tr {
			border-bottom: 1px solid #ddd;
			td {
				padding: 0.5rem;
				text-align: center;
			}
			td:last-child {
				display: flex;
				gap: 1rem;
				justify-content: center;
				button {
					padding: 0;
					display: flex;
					justify-content: center;
					align-items: center;
					width: 50px;
					height: 50px;
					border: 1px solid transparent;
					background-color: transparent;
					ion-icon {
						font-size: 1.5rem;
						color: #000;
					}
				}
				button:last-child {
					ion-icon {
						color: red;
					}
				}
				button:hover {
					background-color: transparent;
					border: 1px solid gray;
				}
			}
		}
		tr:nth-child(even) {
			background-color: $ColorVueBg;
		}
	}
}

/* Small screens */
.card__container {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 1rem;
	width: 100%;
	margin: 1rem 0 3rem 0;
}
.card {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 1rem;
	padding: 1rem;
	border: 1px solid #ccc;
	border-radius: 5px;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
	transition: all 0.3s ease;

	&:hover {
		box-shadow: 0 8px 16px rgba(0, 0, 0, 0.26);
	}
	h2 {
		font-size: 1rem;
		font-weight: 900;
	}
	p {
		span {
			font-weight: bold;
		}
	}
	.card__actions {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 1rem;
		button {
			width: 50px;
			height: 50px;
			border: 1px solid transparent;
			background-color: transparent;
			ion-icon {
				font-size: 1.5rem;
				color: #000;
			}
		}
		button:last-child {
			ion-icon {
				color: red;
			}
		}
	}
}
.card:nth-child(even) {
	background-color: $ColorVueBg;
}
.buttons {
	position: fixed;
	z-index: 10;
	bottom: 0;
	left: 0;
	right: 0;
	display: flex;
	justify-content: center;
	align-items: center;
	gap: 1rem;
	padding: 1rem;
	button {
		display: flex;
		justify-content: center;
		align-items: center;
		border-radius: 50%;
		width: 50px;
		height: 50px;
		border: 1px solid transparent;
		background-color: var(--bs-blue);
		ion-icon {
			font-size: 1.5rem;
			color: #000;
		}
	}
	span {
		display: none;
	}
	@media (min-width: 767px) {
		position: inherit;
		button {
			width: 200px;
			border-radius: 10px;
		}
		span {
			display: block;
		}
		ion-icon {
			display: none;
		}
	}
}
</style>
