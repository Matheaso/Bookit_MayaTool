import random
from maya import cmds
from bookit import utils as utl


class BookitTool:
    def __init__(self):
        self.meshes = []
        self.preview_books = []

        self.curve = None
        self.curve_shape_job = None
        self.last_seed = None
        self.preview_group = None

        self.delete_percent = 0
        self.rotation_value = 0

        self.rotate = True
        self.auto_select = False
        self.is_instancing = True

    def ensure_preview_group(self):
        if self.preview_group and cmds.objExists(self.preview_group):
            return self.preview_group

        self.preview_group = cmds.group(empty=True, name="bookit_preview")
        return self.preview_group

    def bake(self):
        if not self.preview_group or not cmds.objExists(self.preview_group):
            cmds.warning("Nothing to bake!")
            return

        self.preview_group = cmds.rename(self.preview_group, "bookit_result")
        self.preview_books = []
        self.preview_group = None


    def kill_curve_shape_job(self):
        if self.curve_shape_job and cmds.scriptJob(exists=self.curve_shape_job):
            cmds.scriptJob(kill=self.curve_shape_job, force=True)

        self.curve_shape_job = None


    def watch_curve_shape(self):
        self.kill_curve_shape_job()
        if not self.curve or not cmds.objExists(self.curve):
            return

        shapes = cmds.listRelatives(self.curve, shapes=True, fullPath=True) or []

        if not shapes:
            cmds.warning("Curve has no shape!")
            return

        shape = shapes[0]

        self.curve_shape_job = cmds.scriptJob(
            attributeChange=[
                f"{shape}.controlPoints",
                self.on_curve_shape_changed
            ],
            protected=True
        )

    def on_curve_shape_changed(self):
        self.generate(self.last_seed)


    def set_books_from_selection(self):
        self.meshes = []
        objs = cmds.ls(selection=True) or []

        if not objs:
            cmds.warning('Nothing selected!')
            return []

        for obj in objs:
            if utl.is_mesh(obj):
                self.meshes.append(obj)

        if not self.meshes:
            cmds.warning('No meshes selected!')
        return self.meshes


    def clear_preview_books(self):

        if self.preview_books:
            cmds.delete(self.preview_group)
            self.preview_group = None
            self.preview_books = []


    def cleanup(self):
        self.kill_curve_shape_job()
        self.clear_preview_books()


    def generate(self, seed):
        cmds.undoInfo(openChunk=True)
        try:
            self.last_seed = seed
            prev_selection = cmds.ls(selection=True) or []


            if not self.meshes:
                cmds.warning("No Meshes")
                return

            selection = cmds.ls(selection=True) or []
            if selection and utl.is_curve(selection[0]):
                    self.curve = selection[0]
                    self.watch_curve_shape()

            for book in self.preview_books:
                if cmds.objExists(book):
                    cmds.delete(book)

            self.preview_books = []

            rng = random.Random(int(seed))

            books = self.meshes[:]
            rng.shuffle(books)

            current_distance = 0.0
            curve_length = utl.get_curve_length(self.curve)

            offset = 0.1

            preview_group = self.ensure_preview_group()

            while current_distance < curve_length:
                source_book = rng.choice(books)


                book_bbox = utl.BBox(source_book)

                width = book_bbox.z

                if current_distance + width + offset * 2 > curve_length:
                    break

                if rng.uniform(0, 100) < self.delete_percent:
                    current_distance += width + offset
                    continue

                if self.is_instancing:
                    new_book = cmds.instance(source_book, name=f"{source_book}_inst_bookit#")[0]
                else:
                    new_book = cmds.duplicate(source_book, name=f"{source_book}_bookit#")[0]

                cmds.parent(new_book, preview_group)

                sample_distance = current_distance + width * 0.5
                percent = sample_distance / curve_length

                pos = utl.sample_curve_at_percent(self.curve, percent)

                next_percent = min(percent + 0.001, 1)
                next_pos = utl.sample_curve_at_percent(self.curve, next_percent)

                rot_y = utl.get_y_rotation_from_points(pos, next_pos)

                rot_offset = rng.uniform(-2, 2)

                pos_offset = utl.offset_side_curve(pos, next_pos, rng.uniform(-0.2, 0.2))

                if self.rotate:
                    cmds.xform(
                        new_book,
                        worldSpace=True,
                        translation=(
                            pos_offset[0] - book_bbox.x * 0.5 ,
                            pos_offset[1],
                            pos_offset[2],
                        ),
                        rotation=(0, rot_y + rot_offset + self.rotation_value, 0)
                    )
                else:
                    cmds.xform(
                        new_book,
                        worldSpace=True,
                        translation=(
                            pos_offset[0] - book_bbox.x * 0.5,
                            pos_offset[1] ,
                            pos_offset[2] ,
                        ),
                        rotation=(0,self.rotation_value, 0)
                    )

                self.preview_books.append(new_book)

                current_distance += width + offset
            if self.auto_select:
                cmds.select(self.preview_books)
            else:
                if prev_selection:
                    cmds.select(prev_selection, replace=True)

            cmds.setFocus("MayaWindow")
        finally:
            cmds.undoInfo(closeChunk=True)
