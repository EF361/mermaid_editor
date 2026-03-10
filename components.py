# components.py (FULL FILE)
import streamlit.components.v1 as components
import html
def mermaid(code, title="diagram", height=750):
    # Escape code to prevent HTML injection issues
    safe_code = html.escape(code)

    html_content = f"""
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8"/>
      <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
      <style>
        :root {{
          --bg: #ffffff;
          --toolbar-bg: rgba(250,250,250,0.9);
          --btn-bg: #f3f4f6;
          --btn-hover: #e6e7ea;
        }}

        html,body {{
          margin:0;
          padding:0;
          background:var(--bg);
          font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
        }}

        .preview-wrapper {{
          position: relative;
          width: 100%;
          min-height: 60vh;
          box-sizing: border-box;
          padding: 24px;
          display:flex;
          justify-content:center;
          align-items:flex-start;
        }}

        /* Toolbar in top-right of preview container (relative to wrapper) */
        .toolbar {{
          position: absolute;
          right: 18px;
          top: 12px;
          display:flex;
          gap:8px;
          z-index: 20;
          background: var(--toolbar-bg);
          padding:6px;
          border-radius:8px;
          box-shadow: 0 6px 16px rgba(0,0,0,0.04);
        }}

        .toolbar button {{
          border: none;
          background: var(--btn-bg);
          padding:8px 10px;
          border-radius:8px;
          cursor:pointer;
          font-size:14px;
        }}

        .toolbar button:hover {{ background: var(--btn-hover); }}

        /* Constrain mermaid container and ensure svg responsive */
        #diagram-container {{
          width: 100%;
          max-width: 880px; /* limits huge diagrams */
          box-sizing: border-box;
        }}

        .mermaid svg {{
          width: 100% !important;
          height: auto !important;
          display:block;
        }}

        /* If mermaid renders into an <svg> inside the container, center it */
        #diagram-container > svg, #diagram-container svg {{
          display:block;
          margin: 0 auto;
          max-width: 880px;
          height:auto;
        }}

      </style>
    </head>
    <body>

      <div class="preview-wrapper">
        <div class="toolbar" role="toolbar" aria-label="diagram actions">
          <button id="downloadBtn" title="Export PNG">🖼</button>
          <button id="copyBtn" title="Copy PNG">📋</button>
        </div>

        <div id="diagram-container" class="mermaid">
{safe_code}
        </div>
      </div>

      <script>
        // initialize mermaid and render content already present
        mermaid.initialize({{ startOnLoad: true }});

        // Helpers for filename
        const diagramTitle = "{title}".replace(/[^a-z0-9\\-\\_ ]/gi,'_').trim();
        function timestamp() {{
          const now = new Date();
          const yyyy = now.getFullYear();
          const mm = String(now.getMonth()+1).padStart(2,'0');
          const dd = String(now.getDate()).padStart(2,'0');
          const hh = String(now.getHours()).padStart(2,'0');
          const min = String(now.getMinutes()).padStart(2,'0');
          return `${{yyyy}}-${{mm}}-${{dd}}_${{hh}}-${{min}}`;
        }}

        // Convert the rendered SVG to PNG using an Image + canvas at proper DPR
        async function svgToCanvas(svgElement) {{
          // Serialize SVG
          const serializer = new XMLSerializer();
          const svgString = serializer.serializeToString(svgElement);

          // Create blob + url
          const blob = new Blob([svgString], {{type: 'image/svg+xml;charset=utf-8'}});
          const url = URL.createObjectURL(blob);

          // Load into image
          const img = new Image();
          // preserve transparency
          img.crossOrigin = "anonymous";

          await new Promise((resolve, reject) => {{
            img.onload = () => resolve();
            img.onerror = (e) => reject(e);
            img.src = url;
          }});

          const dpr = window.devicePixelRatio || 1;
          const canvas = document.createElement('canvas');
          canvas.width = Math.round(img.width * dpr);
          canvas.height = Math.round(img.height * dpr);

          const ctx = canvas.getContext('2d');
          ctx.setTransform(dpr, 0, 0, dpr, 0, 0); // scale for DPR
          ctx.drawImage(img, 0, 0);

          URL.revokeObjectURL(url);
          return canvas;
        }}

        function getRenderedSVG() {{
          // Mermaid usually produces an <svg> inside the mermaid container
          const container = document.getElementById('diagram-container');
          if (!container) return null;
          const svg = container.querySelector('svg');
          return svg;
        }}

        async function generateCanvas() {{
          // prefer rendering the svg itself (crisper than html2canvas)
          const svg = getRenderedSVG();
          if (svg) {{
            try {{
              const canvas = await svgToCanvas(svg);
              return canvas;
            }} catch (e) {{
              console.warn('svg->canvas failed, fallback to html2canvas', e);
            }}
          }}

          // fallback: capture the container using html2canvas
          if (!window.html2canvasFallback) {{
            // lazy load html2canvas only if fallback required
            const s = document.createElement('script');
            s.src = 'https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js';
            document.head.appendChild(s);
            await new Promise(resolve => s.onload = resolve);
            window.html2canvasFallback = window.html2canvas;
          }}

          const container = document.getElementById('diagram-container');
          const canvas = await window.html2canvasFallback(container, {{ backgroundColor: null, scale: window.devicePixelRatio || 1}});
          return canvas;
        }}

        // Download PNG
        document.getElementById('downloadBtn').addEventListener('click', async () => {{
          try {{
            const canvas = await generateCanvas();
            const filename = `${{diagramTitle}} - ${{timestamp()}}.png`;
            const link = document.createElement('a');
            link.download = filename;
            link.href = canvas.toDataURL('image/png');
            link.click();
          }} catch (e) {{
            alert('Failed to export PNG: ' + e);
            console.error(e);
          }}
        }});

        // Copy to clipboard (PNG)
        document.getElementById('copyBtn').addEventListener('click', async () => {{
          try {{
            const canvas = await generateCanvas();
            await new Promise((resolve, reject) => {{
              canvas.toBlob(async (blob) => {{
                try {{
                  await navigator.clipboard.write([ new ClipboardItem({{ 'image/png': blob }}) ]);
                  resolve();
                }} catch (err) {{
                  reject(err);
                }}
              }}, 'image/png');
            }});
            // small UX cue
            const tmp = document.createElement('div');
            tmp.style.position='fixed'; tmp.style.left='10px'; tmp.style.top='10px';
            tmp.style.padding='8px 12px'; tmp.style.background='rgba(0,0,0,0.7)'; tmp.style.color='white';
            tmp.style.borderRadius='6px'; tmp.style.zIndex = 9999;
            tmp.textContent = 'PNG copied to clipboard';
            document.body.appendChild(tmp);
            setTimeout(()=>tmp.remove(), 1300);
          }} catch (e) {{
            alert('Copy failed: ' + e + '\\nNote: some browsers restrict clipboard image writes.');
            console.error(e);
          }}
        }});
      </script>
    </body>
    </html>
    """

    components.html(html_content, height=height, scrolling=True)