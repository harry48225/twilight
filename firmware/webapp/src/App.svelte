<script lang="ts">
import BlindGraphic from "./BlindGraphic.svelte";
import Header from "./Header.svelte";
import Scheduler from "./Scheduler.svelte";
import SunPositionTable from "./SunPositionTable.svelte";

let height = 512;
</script>

<Header/>
<main>
	<SunPositionTable/>
	<button on:click={() => fetch("/api/lower_blind")}>lower</button>
	<button on:click={() => fetch("/api/raise_blind")}>raise</button>
	<Scheduler/>
	<BlindGraphic height={height}/>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 800px;
		margin: 0 auto;
	}
</style>