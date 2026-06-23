# components.py
import streamlit as st
import html
import json

def mermaid(code, title="diagram", height=750):
    # Escape code to prevent HTML injection issues in the HTML markup
    safe_code = html.escape(code)
    
    # Safe JSON dump to pass code directly to JavaScript without syntax errors
    js_code = json.dumps(code)

    html_content = f"""
    <head>
      <meta charset="utf-8"/>
      <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.6.1/dist/svg-pan-zoom.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
      <style>
        :root {{
          --bg: #ffffff;
          --toolbar-bg: rgba(255, 255, 255, 0.95);
          --btn-bg: #f3f4f6;
          --btn-hover: #e5e7eb;
          --btn-active: #d1d5db;
          --btn-text: #374151;
        }}

        html, body {{
          margin: 0;
          padding: 0;
          width: 100%;
          height: 100%;
          overflow: hidden;
          background: var(--bg);
          font-family: Inter, system-ui, -apple-system, sans-serif;
        }}

        .preview-wrapper {{
          width: 100%;
          height: 100vh;
          display: flex;
          flex-direction: column;
          background: #fafafa;
          box-sizing: border-box;
          overflow: hidden;
        }}

        /* Toolbar as a dedicated top-bar header */
        .toolbar {{
          display: flex;
          align-items: center;
          justify-content: flex-start;
          flex-wrap: wrap;
          gap: 8px;
          z-index: 100;
          background: #ffffff;
          padding: 10px 16px;
          border-bottom: 1px solid #e5e7eb;
          box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        }}

        .toolbar button {{
          border: 1px solid #e5e7eb;
          background: #ffffff;
          color: var(--btn-text);
          padding: 6px 12px;
          border-radius: 6px;
          cursor: pointer;
          font-size: 12px;
          font-weight: 600;
          transition: all 0.15s ease;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 6px;
          outline: none;
        }}

        .toolbar button:hover {{
          background: #f9fafb;
          border-color: #d1d5db;
          color: #111827;
        }}

        .toolbar button:active {{
          background: #f3f4f6;
        }}

        .toolbar .divider {{
          width: 1px;
          height: 20px;
          background: #e5e7eb;
          margin: 0 4px;
        }}

        /* Dedicated container for the canvas to avoid overlapping */
        .canvas-container {{
          flex: 1;
          position: relative;
          width: 100%;
          overflow: hidden;
          display: flex;
          align-items: center;
          justify-content: center;
        }}

        #diagram-container {{
          width: 100%;
          height: 100%;
          overflow: hidden;
          cursor: grab;
        }}

        #diagram-container:active {{
          cursor: grabbing;
        }}

        .mermaid {{
          width: 100%;
          height: 100%;
        }}

        .mermaid svg {{
          width: 100% !important;
          height: 100% !important;
          display: block;
        }}
      </style>
    </head>
    <body>

      <div class="preview-wrapper">
        <div class="toolbar" role="toolbar" aria-label="diagram actions">
          <button id="zoomInBtn" title="Zoom In">➕ Zoom In</button>
          <button id="zoomOutBtn" title="Zoom Out">➖ Zoom Out</button>
          <button id="resetBtn" title="Reset View">🎯 Reset View</button>
          <div class="divider"></div>
          <button id="copyCodeBtn" title="Copy Mermaid Code">📄 Copy Code</button>
          <button id="copyBtn" title="Copy PNG Image">📋 Copy PNG</button>
          <button id="downloadBtn" title="Export PNG Image">🖼 Export PNG</button>
        </div>
        <div class="canvas-container">
          <div id="diagram-container" class="mermaid">
{safe_code}
          </div>
        </div>
      </div>

      <script>
        // Configure Mermaid
        mermaid.initialize({{
          startOnLoad: false,
          theme: 'default',
          securityLevel: 'loose',
          flowchart: {{ useHtmlLabels: false }},
          sequence: {{ useHtmlLabels: false }},
          gantt: {{ useHtmlLabels: false }}
        }});

        // Toast utility
        function showToast(message) {{
          const oldToast = document.getElementById('app-toast');
          if (oldToast) oldToast.remove();

          const tmp = document.createElement('div');
          tmp.id = 'app-toast';
          tmp.style.position = 'fixed'; 
          tmp.style.left = '50%'; 
          tmp.style.bottom = '20px';
          tmp.style.transform = 'translateX(-50%)';
          tmp.style.padding = '8px 16px'; 
          tmp.style.background = '#1f2937'; 
          tmp.style.color = '#f9fafb';
          tmp.style.borderRadius = '6px'; 
          tmp.style.zIndex = 9999;
          tmp.style.boxShadow = '0 10px 15px -3px rgba(0, 0, 0, 0.1)';
          tmp.style.fontSize = '13px';
          tmp.style.fontWeight = '500';
          tmp.style.transition = 'opacity 0.2s';
          tmp.style.pointerEvents = 'none';
          tmp.textContent = message;
          document.body.appendChild(tmp);
          setTimeout(() => {{
            tmp.style.opacity = '0';
            setTimeout(() => tmp.remove(), 200);
          }}, 1500);
        }}

        // Helpers for filename
        const diagramTitle = "{title}".replace(/[^a-z0-9\\-\\_ ]/gi,'_').trim() || "diagram";
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
          const serializer = new XMLSerializer();
          
          // Clone the SVG so we don't mutate the displayed one
          const clonedSvg = svgElement.cloneNode(true);
          
          // Explicitly set width & height from viewBox attributes to ensure full crisp resolution in serialized image
          const viewBox = clonedSvg.getAttribute('viewBox');
          if (viewBox) {{
            const parts = viewBox.split(' ');
            if (parts.length === 4) {{
              const w = parseFloat(parts[2]);
              const h = parseFloat(parts[3]);
              clonedSvg.setAttribute('width', w + 'px');
              clonedSvg.setAttribute('height', h + 'px');
              clonedSvg.removeAttribute('style');
            }}
          }}

          const svgString = serializer.serializeToString(clonedSvg);

          // Create blob + url
          const blob = new Blob([svgString], {{type: 'image/svg+xml;charset=utf-8'}});
          const url = URL.createObjectURL(blob);

          // Load into image
          const img = new Image();
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
          const container = document.getElementById('diagram-container');
          if (!container) return null;
          return container.querySelector('svg');
        }}

        async function generateCanvas() {{
          // Temporarily reset pan & zoom to get a clean complete capture of the diagram
          let panState = null;
          if (window.panZoom) {{
            panState = {{
              zoom: window.panZoom.getZoom(),
              pan: window.panZoom.getPan()
            }};
            window.panZoom.reset();
            window.panZoom.fit();
            window.panZoom.center();
          }}

          const svg = getRenderedSVG();
          let canvas = null;
          if (svg) {{
            try {{
              const tempCanvas = await svgToCanvas(svg);
              // Test if canvas is tainted
              const ctx = tempCanvas.getContext('2d');
              ctx.getImageData(0, 0, 1, 1); // Will throw SecurityError if tainted
              canvas = tempCanvas;
            }} catch (e) {{
              console.warn('SVG canvas rendering failed or is tainted, falling back to html2canvas:', e);
            }}
          }}

          if (!canvas) {{
            try {{
              const container = document.getElementById('diagram-container');
              // html2canvas is preloaded in the head tag
              canvas = await html2canvas(container, {{
                backgroundColor: null,
                scale: window.devicePixelRatio || 1,
                logging: false,
                useCORS: true
              }});
            }} catch (err) {{
              console.error('html2canvas fallback failed:', err);
            }}
          }}

          // Restore panZoom state if active
          if (window.panZoom && panState) {{
            window.panZoom.zoom(panState.zoom);
            window.panZoom.pan(panState.pan);
          }}

          if (!canvas) {{
            throw new Error('Canvas generation failed');
          }}

          return canvas;
        }}

        // Toolbar actions setup
        document.getElementById('zoomInBtn').addEventListener('click', () => {{
          if (window.panZoom) window.panZoom.zoomIn();
        }});

        document.getElementById('zoomOutBtn').addEventListener('click', () => {{
          if (window.panZoom) window.panZoom.zoomOut();
        }});

        document.getElementById('resetBtn').addEventListener('click', () => {{
          if (window.panZoom) {{
            window.panZoom.reset();
            window.panZoom.fit();
            window.panZoom.center();
          }}
        }});

        // Copy raw code
        const rawCode = {js_code};
        document.getElementById('copyCodeBtn').addEventListener('click', async () => {{
          try {{
            await navigator.clipboard.writeText(rawCode);
            showToast('Code copied to clipboard');
          }} catch (e) {{
            // Text copy fallback
            try {{
              const textarea = document.createElement('textarea');
              textarea.value = rawCode;
              textarea.style.position = 'fixed';
              document.body.appendChild(textarea);
              textarea.select();
              document.execCommand('copy');
              document.body.removeChild(textarea);
              showToast('Code copied to clipboard');
            }} catch (err) {{
              alert('Failed to copy code: ' + err);
            }}
          }}
        }});

        // Copy PNG to clipboard
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
            showToast('PNG copied to clipboard');
          }} catch (e) {{
            alert('Copy failed: ' + e + '\\nNote: clipboard writes might be restricted in some browsers/contexts.');
            console.error(e);
          }}
        }});

        // Download PNG
        document.getElementById('downloadBtn').addEventListener('click', async () => {{
          try {{
            const canvas = await generateCanvas();
            const filename = `${{diagramTitle}} - ${{timestamp()}}.png`;
            const link = document.createElement('a');
            link.download = filename;
            link.href = canvas.toDataURL('image/png');
            link.click();
            showToast('PNG downloaded');
          }} catch (e) {{
            alert('Failed to export PNG: ' + e);
            console.error(e);
          }}
        }});

        // Setup svg-pan-zoom on the svg
        function setupPanZoom() {{
          const container = document.getElementById('diagram-container');
          if (!container) return;
          const svgElement = container.querySelector('svg');
          if (!svgElement) return;

          svgElement.style.width = '100%';
          svgElement.style.height = '100%';
          svgElement.style.maxWidth = 'none';

          window.panZoom = svgPanZoom(svgElement, {{
            zoomEnabled: true,
            controlIconsEnabled: false,
            fit: true,
            center: true,
            minZoom: 0.1,
            maxZoom: 10,
            zoomScaleSensitivity: 0.2
          }});
        }}

        async function init() {{
          try {{
            await mermaid.run();
            setupPanZoom();
          }} catch (err) {{
            console.error("Mermaid run failed:", err);
          }}
        }}

        if (document.readyState === 'loading') {{
          window.addEventListener('DOMContentLoaded', init);
        }} else {{
          init();
        }}
      </script>
    </body>
    </html>
    """

    # We escape the html content to safely inject inside srcdoc, and replace newlines with HTML entities.
    # This keeps the markdown string on a single line so Streamlit's parser renders it as raw HTML instead of a code block.
    escaped_html = html.escape(html_content).replace('\n', '&#10;').replace('\r', '')
    
    iframe_code = f'<iframe srcdoc="{escaped_html}" width="100%" height="{height}px" style="border: 1px solid #e5e7eb; border-radius: 12px; overflow: hidden; background: #ffffff;" allow="clipboard-write"></iframe>'
    
    st.markdown(iframe_code, unsafe_allow_html=True)