<script>
	import { onMount } from 'svelte';
	export let eel;
	export let index;

	let machines = [];
    let loading = false

	onMount(async () => {
		machines = await list();	
		console.log(machines)
	});

	async function list() {
		return await eel.list_machines(index)();
	}

    async function refetch() {
        console.log("Inside refetch")
        machines = await eel.list_state()();
        console.log(machines)
    }

    async function start() {
        loading = true
        await eel.start_environment()();
        refetch();
        loading = false
        console.log("after return")
    }
    async function stop() {
        loading = true
        await eel.stop_environment()();
        refetch();
        loading = false
        console.log("after return")
    }
</script>

<ul>
    {#each machines as machine}
        <li>{machine.name}: {machine.state}</li>
    {/each}
    <button on:click={async () => await start()}>{loading ? "Loading.. This may take a while" : "Start Machines"}</button>
    <button on:click={async () => await stop()}>{loading ? "Loading.. This may take a while" : "Stop Machines"}</button>
</ul>
