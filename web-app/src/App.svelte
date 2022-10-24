<!-- <svelte:head>
	<script type="text/javascript" src="http://localhost:8080/eel.js"></script>
</svelte:head> -->

<script>
	import { onMount } from 'svelte';
	import { selectedChallenge, challenges } from './lib/stores'

	/** svelte components **/
	import Challenge from './components/Challenge.svelte'
    import Sidebar from './components/Sidebar.svelte';
    import Loading from './components/Loading.svelte';
	
	/** props **/
	export let eel;

	eel.set_host('ws://localhost:8080')

	onMount(async () => {
		$challenges = await fetchChallenges();
		console.log($challenges);
	});

	async function fetchChallenges() {
		let c = await eel.list_challenges()();
		return c;
	}
</script>

<main class="flex w-full h-full py-4 text-white">
	<Sidebar eel={eel}></Sidebar>
	
	<div class="p-8 w-full">
	{#if $selectedChallenge === ""}
		<p>
			Creating machines for the first time may take a while. Please be patient!
		</p>
	{:else}
		<Challenge eel={eel} />
	{/if}
	</div>
</main>

