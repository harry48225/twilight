<script lang="ts">
import Header from "./Header.svelte";
import SunPositionTable from "./SunPositionTable.svelte";

</script>

<Header/>
<main>
	<SunPositionTable/>
	<button>lower</button>
	<button>raise</button>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 800px;
		margin: 0 auto;
	}
</style>