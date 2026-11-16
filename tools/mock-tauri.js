(function () {
  var cbs = {}, nextId = 1, listeners = {}, nextEv = 1;
  var settings = {
    version: 2, ceremonyEnabled: true, autostartEnabled: true, weekdaysOnly: false,
    preset: "voice_metronome", blocks: ["announcement", "metronome"], volume: 80,
    pauseOtherPlayers: true, resumeAfterCeremony: false, showVisualOverlay: false,
    showFlagAnimation: false, showNearbyPersonalDates: false, systemTimeOnly: false,
    volumePriority: false, autoUnmute: false, ntpServer: "time.google.com",
    lateStartGraceMinutes: 1, reminderEnabled: false, reminderMinutesBefore: 5,
    announcementVoice: "bohdan_hdal", anthemVoice: "default", useSystemTheme: true,
    uiTheme: "light", lastShownNearbyDateId: null, skipDate: null
  };
  var status = { ceremonyActive: false, skipTomorrow: false, lastActivation: "2026-11-16 09:00:00", lastNtpSync: "2026-11-16 08:59:12" };
  var voices = ["bohdan_hdal", "sonia_sotnyk", "dania_khomutovskyi", "radio_bg", "vinnytsia_city"].map(function (v) {
    return { voice: v, hasEnding: true, announcementIncludesBell: false };
  });
  function emit(event, payload) {
    (listeners[event] || []).forEach(function (l) {
      var f = window["_" + l.handler]; if (f) f({ event: event, id: l.id, payload: payload });
    });
  }
  async function decodeApng(bytes) {
    var dec = new ImageDecoder({ data: new Uint8Array(bytes), type: "image/png" });
    await dec.tracks.ready;
    var n = dec.tracks.selectedTrack.frameCount, frames = [], w = 0, h = 0;
    for (var i = 0; i < n; i++) {
      var r = await dec.decode({ frameIndex: i }), img = r.image;
      w = img.displayWidth; h = img.displayHeight;
      var c = new OffscreenCanvas(w, h), x = c.getContext("2d");
      x.drawImage(img, 0, 0); img.close();
      var u8 = new Uint8Array(x.getImageData(0, 0, w, h).data.buffer), bin = "";
      for (var j = 0; j < u8.length; j += 0x8000) bin += String.fromCharCode.apply(null, u8.subarray(j, j + 0x8000));
      frames.push(btoa(bin));
    }
    return { width: w, height: h, frames: frames };
  }
  window.__mockEmit = emit;
  window.__TAURI_EVENT_PLUGIN_INTERNALS__ = { unregisterListener: function () {} };
  window.__TAURI_INTERNALS__ = {
    metadata: { currentWindow: { label: "main" }, currentWebview: { windowLabel: "main", label: "main" } },
    transformCallback: function (cb) { var id = nextId++; window["_" + id] = cb; return id; },
    unregisterCallback: function (id) { delete window["_" + id]; },
    convertFileSrc: function (p) { return p; },
    invoke: function (cmd, args) {
      switch (cmd) {
        case "get_initial_state": return Promise.resolve({ settings: settings, personalDates: [], status: status, version: "0.7.0", voices: voices });
        case "decode_apng_frames": return decodeApng(args.data);
        case "get_status": return Promise.resolve(status);
        case "check_for_updates": return Promise.resolve(null);
        case "plugin:event|listen":
          var id = nextEv++; (listeners[args.event] = listeners[args.event] || []).push({ id: id, handler: args.handler });
          return Promise.resolve(id);
        case "plugin:event|unlisten": return Promise.resolve();
        case "trigger_ceremony_now": return new Promise(function (res) { window.__finish = res; setTimeout(function () { emit("ceremony-start", { duration_ms: 60000, is_test: true }); window.__endT = setTimeout(function () { emit("ceremony-end", null); if (window.__finish) { window.__finish(); window.__finish = null; } }, 60000); }, 150); });
        case "stop_test_ceremony": clearTimeout(window.__endT); emit("ceremony-end", null); if (window.__finish) { window.__finish(); window.__finish = null; } return Promise.resolve();
        default: return Promise.resolve(null);
      }
    }
  };
})();
