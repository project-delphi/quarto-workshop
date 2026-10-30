// Relief view (slides/_water.qmd, #water-relief): one column per clustered urban zone, at
// its municipality's centroid, as tall as its head town's altitude (exaggerated) and
// coloured by cluster, standing on the national and department borders. The deck cell
// computes the columns and borders in km; this scene only draws them (stage.js). Altitude
// is the scene's y axis, so the stage turns the map about its vertical; north is -z.
import {
  BoxGeometry, BufferAttribute, BufferGeometry, DirectionalLight, HemisphereLight,
  InstancedMesh, LineBasicMaterial, LineSegments, MeshLambertMaterial, Object3D,
} from "three";

export const relief = {
  views: (data) => ({
    flat: { rx: Math.PI / 2, ry: 0, zoom: 1, spin: 0, focus: false },     // the map from above
    tilt: { rx: Math.PI / 2 - 1.0, ry: 0, zoom: 1.4, spin: 0, focus: false }, // the columns rise
    // Into the highlands: turn about the highest cluster's middle column, closer and slowly.
    focus: { rx: 0.45, ry: 0.5, zoom: 2.2, spin: 0.06, focus: true,
             centre: [data.view[0], data.view[2], -data.view[1]] },
  }),

  build(group, data) {
    const [x0, x1, y0, y1] = data.extent;
    const half = Math.max(x1 - x0, y1 - y0) / 2;
    const width = half * 0.014; // column footprint, km
    const box = new BoxGeometry(1, 1, 1).translate(0, 0.5, 0); // stands on the map
    const place = new Object3D();
    const materials = data.clusters.map((c) => {
      const rows = [];
      for (let i = 0; i < data.cols.length; i += 4) if (data.cols[i + 3] === c.id) rows.push(i);
      const material = new MeshLambertMaterial({ color: c.color, transparent: true });
      material.userData.id = c.id;
      const mesh = new InstancedMesh(box, material, rows.length);
      rows.forEach((i, j) => {
        const h = Math.max((data.cols[i + 2] / 1000) * data.exaggeration, width * 0.3);
        place.position.set(data.cols[i], 0, -data.cols[i + 1]);
        place.scale.set(width, h, width);
        place.updateMatrix();
        mesh.setMatrixAt(j, place.matrix);
      });
      group.add(mesh);
      return material;
    });

    const lines = (flat, opacity) => {
      const pos = new Float32Array((flat.length / 2) * 3);
      for (let i = 0, j = 0; i < flat.length; i += 2, j += 3) {
        pos[j] = flat[i];
        pos[j + 2] = -flat[i + 1];
      }
      const geometry = new BufferGeometry();
      geometry.setAttribute("position", new BufferAttribute(pos, 3));
      group.add(new LineSegments(geometry,
        new LineBasicMaterial({ color: 0xb8c2cc, transparent: true, opacity })));
    };
    lines(data.outline, 0.8);
    lines(data.departments, 0.25);

    // Sky from above and sun from the north-west; both turn with the map.
    const sky = new HemisphereLight(0xffffff, 0x3a3a3a, 1.8);
    const sun = new DirectionalLight(0xffffff, 1.6);
    sun.position.set((x0 + x1) / 2 - half, half * 2, -(y1 + half));
    sun.target.position.set((x0 + x1) / 2, 0, -(y0 + y1) / 2);
    group.add(sky, sun, sun.target);

    return {
      centre: [(x0 + x1) / 2, 0, -(y0 + y1) / 2],
      half,
      aspect: (x1 - x0) / (y1 - y0),
      labels: [],
      focus(t) {
        materials.forEach((m) => {
          m.opacity = data.focus.includes(m.userData.id) ? 1 : 1 - 0.8 * t;
          m.depthWrite = m.opacity > 0.99;
        });
      },
    };
  },
};
