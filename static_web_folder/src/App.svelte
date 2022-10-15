<!-- <svelte:head>
	<script type="text/javascript" src="http://localhost:8080/eel.js"></script>
</svelte:head> -->

<script>
	import { onMount } from 'svelte';
	import Challenge from './components/Challenge.svelte'
	export let eel;

	function set_challenge(index) {
		selected_challenge = index
		console.log(selected_challenge);
	}
	let selected_challenge = ""

	eel.set_host('ws://localhost:8080')

	let challenges = [];

	onMount(async () => {
		challenges = await run();	
		console.log(challenges)
	});

	async function run() {
		let machines = await eel.list_challenges()();
		
		return machines;
	}
</script>

<main>
	<h1>Purple Dome CTF</h1>
	{#if selected_challenge === ""}
		<ul>
		{#each challenges as challenge}
			<li>
				<button on:click={() => set_challenge(challenge)}>{challenge}</button>
			</li>
		{/each}
		</ul>
	{:else}
		<button on:click={() => set_challenge("")}>Back</button>
		<Challenge eel={eel} index={selected_challenge} />
	{/if}

</main>

<style>
	main {
		padding: 1em;
		margin: 0;
	}
</style>
