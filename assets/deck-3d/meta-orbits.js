// Orbit rings (slides/_water.qmd, #water-meta-orbits): each cluster is a body whose ring
// radius is the distance of its mean from the all-municipality mean on Saber 11 and infant
// mortality, whose direction is that bearing and whose height is its mean dropout. Its
// municipalities circle it, spread as in the data. A new clustering pulls bodies along
// springs to their new rings, swinging past and settling; extra clusters grow out of the
// centre. The deck cell computes radii, bearings, counts and the sample of members.
import {
  BufferAttribute, BufferGeometry, Color, LineBasicMaterial, LineLoop, LineSegments, Mesh,
  MeshLambertMaterial, Points, PointsMaterial, SphereGeometry, Vector3,
} from "three";
import { frame, lights, palette, world } from "./meta.js";

const RING = 64, STIFF = 22, DAMP = 6.5;
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
    // [r, bearing, height, size] per slot: current, target, velocity.
    const cur = Array.from({ length: slots }, () => [0, 0, 0, 0]);
    const tgt = cur.map((c) => c.slice()), vel = cur.map(() => [0, 0, 0, 0]);
    const parts = colors.map((color, c) => {
      const body = new Mesh(new SphereGeometry(1, 24, 16), new MeshLambertMaterial({ color }));
      const ringGeo = new BufferGeometry().setFromPoints(
        Array.from({ length: RING }, (_, i) => new Vector3(Math.cos((2 * Math.PI * i) / RING), 0,
          Math.sin((2 * Math.PI * i) / RING))));
      const ring = new LineLoop(ringGeo, new LineBasicMaterial({ color, transparent: true, opacity: 0.75 }));
      const spoke = new LineSegments(new BufferGeometry().setFromPoints([new Vector3(), new Vector3()]),
        new LineBasicMaterial({ color, transparent: true, opacity: 0.25 }));
      const swarm = new Points(new BufferGeometry(), new PointsMaterial({
        color, size: 0.035, sizeAttenuation: true, transparent: true, opacity: 0.9, depthWrite: false }));
      swarm.frustumCulled = false;
      group.add(body, ring, spoke, swarm);
      return { body, ring, spoke, swarm, offsets: [] };
    });
    let clock = 0;

    function place() {
      parts.forEach((p, c) => {
        const [r, a, h, s] = cur[c];
        const x = r * Math.cos(a), z = r * Math.sin(a);
        p.body.position.set(x, h, z);
        p.body.scale.setScalar(Math.max(s, 0.0001));
        p.body.visible = s > 0.004;
        p.ring.visible = p.spoke.visible = p.swarm.visible = p.body.visible;
        p.ring.scale.set(Math.max(r, 0.0001), 1, Math.max(r, 0.0001));
        p.spoke.geometry.setFromPoints([new Vector3(), new Vector3(x, h, z)]);
        // Members circle their body; the swing rate falls with distance, like an orbit.
        const spin = clock * (1.2 / (0.4 + r)) + c, cos = Math.cos(spin), sin = Math.sin(spin);
        const arr = new Float32Array(p.offsets.length * 3 / 2);
        for (let i = 0; i < p.offsets.length; i += 2) {
          const du = p.offsets[i] * 0.8, dv = p.offsets[i + 1] * 0.8;
          arr.set([x + du * cos - dv * sin, h, z + du * sin + dv * cos], (i / 2) * 3);
        }
        p.swarm.geometry.setAttribute("position", new BufferAttribute(arr, 3));
      });
    }

    return world({
      labels: frame(group, el),
      setState(i) {
        const cs = data.states[i].centroids;
        parts.forEach((p, c) => {
          const m = cs[c];
          if (!m) {
            tgt[c][0] = 0;
            tgt[c][3] = 0;
            return;
          }
          // Newly appearing bodies start at the centre, already facing their bearing.
          if (cur[c][3] < 0.004) cur[c][1] = m.theta;
          tgt[c] = [m.r * 6, cur[c][1] + wrap(m.theta - cur[c][1]), m.w * 2.4, 0.05 + 0.1 * Math.sqrt(m.n / data.u.length)];
          p.offsets = data.swarm[i][c];
        });
      },
      animate(dt) {
        const step = Math.min(dt, 0.05);
        clock += Number.isFinite(dt) ? dt : 0;
        let moving = false;
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
