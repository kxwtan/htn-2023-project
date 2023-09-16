function livefeed() {

    useEffect(() => {
        const controller = new AbortController();
        fetch(url, { signal: controller.signal })
          .then(response => { 
            setFrames(URL.createObjectURL)
            // Read stream and store images in 'setFrame' using URL.createObjectURL.
            // Don't forget to call URL.revokeObjectURL when image is no longer needed.
          });
        
        return () => controller.abort();
      });
    return (
        <div>
            <h3 style={{textAlign: 'center'}}>Live Streaming</h3>
            <img src="http://127.0.0.1:5000/video_feed" width="100%"/>
        </div>
    )
}

export default livefeed