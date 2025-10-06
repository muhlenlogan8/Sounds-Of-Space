import { useEffect, useState } from "react";

const App = () => {
	const [currentData, setCurrentData] = useState(null);
	const [currentAudio, setCurrentAudio] = useState(null);
	const [nextData, setNextData] = useState(null);
	const [nextAudio, setNextAudio] = useState(null);

	const fetchData = async (endpoint) => {
		try {
			const res = await fetch(`http://127.0.0.1:5000/${endpoint}`);
			const json = await res.json();
			if (!json.error) {
				// Preload image
				const img = new Image();
				img.src = json.hdurl || json.url;

				// Preload audio
				const audio = new Audio(json.audio_url);
				audio.loop = true;
				audio.load(); // prefetch but don’t play yet

				return { data: json, audio };
			}
		} catch (err) {
			console.error("Fetch error:", err);
		}
		return null;
	};

	// First load
	useEffect(() => {
		(async () => {
			const today = await fetchData("get-today");
			if (today) {
				setCurrentData(today.data);
				today.audio
					.play()
					.catch((err) => console.error("Audio play failed:", err));
				setCurrentAudio(today.audio);
			}

			// Preload next random
			const random = await fetchData("get-random");
			if (random) {
				setNextData(random.data);
				setNextAudio(random.audio);
			}
		})();
	}, []);

	// Handle click → swap to preloaded next
	const handleClick = async () => {
		if (nextData && nextAudio) {
			// Stop current audio
			if (currentAudio) {
				currentAudio.pause();
				currentAudio.currentTime = 0;
			}

			// Switch instantly
			setCurrentData(nextData);
			setCurrentAudio(nextAudio);
			nextAudio.play().catch((err) => console.error("Audio play failed:", err));

			// Preload a new "next" one
			const random = await fetchData("get-random");
			if (random) {
				setNextData(random.data);
				setNextAudio(random.audio);
			}
		}
	};

	if (!currentData) {
		return (
			<div className="flex justify-center items-center h-screen text-white bg-black">
				Loading...
			</div>
		);
	}

	return (
		<div
			className="relative w-screen h-screen overflow-hidden bg-black cursor-pointer"
			onClick={handleClick}
		>
			<img
				src={currentData.hdurl || currentData.url}
				alt={currentData.title}
				className="w-full h-full object-cover animate-breathe"
			/>
			{currentData.copyright && (
				<div className="absolute bottom-2 right-4 text-white text-sm bg-black/40 px-2 py-1 rounded">
					© {currentData.copyright.trim()}
				</div>
			)}
		</div>
	);
};

export default App;
