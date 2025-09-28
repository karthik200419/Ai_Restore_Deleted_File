import pytsk3
import os
import logging

logging.basicConfig(level=logging.INFO)


class DiskScanner:
    def __init__(self, image_path):
        """
        image_path: raw device path (e.g., \\.\C:)
        """
        self.image_path = image_path

        try:
            # Open the disk in read-only mode
            self.img = pytsk3.Img_Info(self.image_path)
            self.fs = pytsk3.FS_Info(self.img)
            logging.info(f"Opened disk image: {image_path}")
        except Exception as e:
            logging.error(f"Failed to open disk: {e}")
            raise

    def scan_deleted_files(self, directory="/"):
        """
        Scan a directory for deleted files.
        Returns a list of deleted file metadata.
        """
        try:
            dir_obj = self.fs.open_dir(path=directory)
            deleted_files = []

            for file in dir_obj:
                try:
                    if file.info.meta and file.info.meta.flags & pytsk3.TSK_FS_META_FLAG_UNALLOC:
                        filename = file.info.name.name.decode("utf-8")
                        deleted_files.append({
                            "name": filename,
                            "inode": file.info.meta.addr,
                            "size": file.info.meta.size
                        })
                        logging.info(f"Deleted file found: {filename}")
                except Exception:
                    continue

            return deleted_files
        except Exception as e:
            logging.error(f"Error scanning directory: {e}")
            return []

    def recover_file(self, inode, output_dir="recovered_files"):
        """
        Recover a file by inode number and save it to output_dir.
        """
        try:
            file_obj = self.fs.open_meta(inode=inode)
            file_data = file_obj.read_random(0, file_obj.info.meta.size)

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            file_path = os.path.join(output_dir, f"recovered_{inode}.bin")
            with open(file_path, "wb") as f:
                f.write(file_data)

            logging.info(f"Recovered file saved: {file_path}")
            return file_path

        except Exception as e:
            logging.error(f"Failed to recover file inode {inode}: {e}")
            return None
