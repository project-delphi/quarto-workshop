// Orbit rings (slides/_water.qmd, #water-meta-orbits): each cluster is a body whose ring
// radius is the distance of its mean from the all-municipality mean on Saber 11 and infant
// mortality (spread x3), whose direction is that bearing and whose height is its mean dropout
// (x2.4). Its municipalities circle it, spread as in the data. A new year pulls the bodies
// along springs to their new rings, swinging past and settling; a focused cluster stays
// bright and the others fade. The deck cell computes radii, bearings, counts and members.
import {
  BufferAttribute, BufferGeometry, LineBasicMaterial, LineLoop, LineSegments, Mesh,
  MeshLambertMaterial, Points, PointsMaterial, SphereGeometry, Vector3,
} from "three";
import { chase, ease, frame, lights, palette, world } from "./meta.js";

const RING = 64, STIFF = 22, DAMP = 6.5, MEMBERS = 30, RADIAL = 6, LIFT = 2.4;
const wrap = (a) => Math.atan2(Math.sin(a), Math.cos(a));

export const metaOrbits = {
  views: () => ({
    flat: { rx: 0.95, ry: 0, zoom: 1.0, spin: 0, focus: false },
  }),

  build(group, data, el) {
    const colors = palette(data), slots = colors.length;
    lights(group);
    const sun = new Mesh(new SphereGeometry(0.06, 24, 16), new MeshLambertMaterial({
      color: 0xfff2b0, emissive: 0xfff2b0, emissiveIntensity: 0.8 }));
    group.add(sun);
    // [r, bearing, height, size] per slot: current, target, velocity; and a fade (1 = bright).
    const cur = Array.from({ length: slots }, () => [0, 0, 0, 0]);
    const tgt = cur.map((c) => c.slice()), vel = cur.map(() => [0, 0, 0, 0]);
    const fade = new Float32Array(slots).fill(1), fadeT = new Float32Array(slots).fill(1);
    const ringPoints = Array.from({ length: RING }, (_, i) => new Vector3(
      Math.cos((2 * Math.PI * i) / RING), 0, Math.sin((2 * Math.PI * i) / RING)));
    const parts = colors.map((color) => {
      const body = new Mesh(new SphereGeometry(1, 24, 16), new MeshLambertMaterial({
        color, transparent: true }));
      const ring = new LineLoop(new BufferGeometry().setFromPoints(ringPoints),
        new LineBasicMaterial({ color, transparent: true }));
      const spoke = new LineSegments(new BufferGeometry().setFromPoints([new Vector3(), new Vector3()]),
        new LineBasicMaterial({ color, transparent: true }));
      // Buffers are made once; each frame only their values change.
      const swarmGeo = new BufferGeometry();
      swarmGeo.setAttribute("position", new BufferAttribute(new Float32Array(MEMBERS * 3), 3));
      const swarm = new Points(swarmGeo, new PointsMaterial({
        color, size: 0.035, sizeAttenuation: true, transparent: true, depthWrite: false }));
      swarm.frustumCulled = false;
      group.add(body, ring, spoke, swarm);
      return { body, ring, spoke, swarm, offsets: [] };
    });
    let clock = 0;

    function place() {
      parts.forEach((p, c) => {
        const [r, a, h, s] = cur[c];
        const x = r * Math.cos(a), z = r * Math.sin(a), f = fade[c];
        p.body.position.set(x, h, z);
        p.body.scale.setScalar(Math.max(s, 0.0001));
        p.body.visible = s > 0.004;
        p.ring.visible = p.spoke.visible = p.swarm.visible = p.body.visible;
        p.body.material.opacity = 0.25 + 0.75 * f;
        p.ring.material.opacity = 0.1 + 0.65 * f;
        p.spoke.material.opacity = 0.05 + 0.25 * f;
        p.swarm.material.opacity = 0.15 + 0.75 * f;
        p.ring.scale.set(Math.max(r, 0.0001), 1, Math.max(r, 0.0001));
        const sp = p.spoke.geometry.attributes.position;
        sp.setXYZ(1, x, h, z);
        sp.needsUpdate = true;
        // Members circle their body; the swing rate falls with distance, like an orbit.
        const spin = clock * (1.2 / (0.4 + r)) + c, cos = Math.cos(spin), sin = Math.sin(spin);
        const arr = p.swarm.geometry.attributes.position, m = p.offsets.length / 2;
        for (let i = 0; i < MEMBERS; i++) {
          if (i >= m) {
            arr.setXYZ(i, x, h, z);
            continue;
          }
          const du = p.offsets[i * 2] * 0.8, dv = p.offsets[i * 2 + 1] * 0.8;
          arr.setXYZ(i, x + du * cos - dv * sin, h, z + du * sin + dv * cos);
        }
        arr.needsUpdate = true;
      });
    }

    let state = 0, focus = 0;
    function retarget() {
      const cs = data.states[state].centroids;
      parts.forEach((p, c) => {
        const m = cs[c];
        fadeT[c] = !focus || focus === c + 1 ? 1 : 0;
        if (!m.n) {
          tgt[c][0] = 0;
          tgt[c][3] = 0;
          p.offsets = [];
          return;
        }
        // A body that was absent starts at the centre, already facing its bearing.
        if (cur[c][3] < 0.004) cur[c][1] = m.theta;
        tgt[c] = [m.r * RADIAL, cur[c][1] + wrap(m.theta - cur[c][1]), m.w * LIFT,
          0.05 + 0.1 * Math.sqrt(m.n / data.u[0].length)];
        p.offsets = data.swarm[state][c];
      });
    }

    return world({
      labels: frame(group, el),
      setState(i) { state = i; retarget(); },
      setCluster(c) { focus = c; retarget(); },
      animate(dt) {
        const step = Math.min(dt, 0.05);
        clock += Number.isFinite(dt) ? dt : 0;
        let moving = chase(fade, fadeT, ease(dt, 4));
        for (let c = 0; c < slots; c++) {
          for (let j = 0; j < 4; j++) {
            if (!Number.isFinite(dt)) {
              cur[c][j] = tgt[c][j];
              vel[c][j] = 0;
              continue;
            }
            vel[c][j] += (STIFF * (tgt[c][j] - cur[c][j]) - DAMP * vel[c][j]) * step;
            cur[c][j] += vel[c][j] * step;
            if (Math.abs(tgt[c][j] - cur[c][j]) > 1e-3 || Math.abs(vel[c][j]) > 1e-3) moving = true;
          }
        }
        place();
        // The swarms keep circling while the slide is shown, unless motion is off (dt = Infinity).
        return moving || Number.isFinite(dt);
      },
    });
  },
};
