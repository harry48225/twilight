<script lang="ts">
import Header from "./Header.svelte";

</script>

<Header/>
<main>
	<button>lower</button>
	<button>raise</button>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>