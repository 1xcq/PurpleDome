<script>
    import { selectedChallenge, runningChallenge, challenges } from "../lib/stores"
    import { onMount } from "svelte";
    import Heading from "./Heading.svelte";
    import Loading from "./Loading.svelte";

    export let eel;

    let isStopping = false;

    async function stop() {
        isStopping = true;
        await eel.stop_running_challenge()();
        console.log("after stopping")
        isStopping = false;
    }

    onMount(async () => {
        $runningChallenge = await eel.get_running_challenge()();
        console.log($runningChallenge);
    })
</script>

<nav class="flex flex-col w-84 gap-4 px-4 py-2 text-white divide-y divide-slate-700 border-r border-slate-700">
	<Heading>
        <button on:click={() => $selectedChallenge = ""}>
            Purple Dome CTF
        </button>
    </Heading>

    <!-- <div class="flex flex-col px-2 pt-4 gap-2"> -->
    <ul class="menu pt-4 text-md gap-2 rounded-none">
        {#each $challenges as challenge, index}
        <li class={index === $selectedChallenge ? "bg-primary rounded-lg" : ""}>
            <button class="rounded-lg" on:click={() => $selectedChallenge = index}>{challenge.name}</button>
        </li>
        {/each}
    </ul>


    <div class="pt-4 px-4 text-sm font-semibold flex flex-col gap-4">
        <div>
            Running: {$challenges[$runningChallenge]?.name || "None"}
        </div>
        <button on:click={async () => await stop()} class="btn btn-error">
            
            {#if isStopping}
                <Loading></Loading>STOPPING
            {:else}
                STOP MACHINES
            {/if}
        </button>
    </div>
</nav>