import { useState, useRef } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Camera, Loader2, X, Upload } from 'lucide-react';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import api from '@/services/api';
import toast from 'react-hot-toast';
import { useAuthStore } from '@/store/authStore';

interface AvatarUploadProps {
  currentAvatar?: string;
  userName: string;
  onSuccess?: (newAvatarUrl: string) => void;
}

export default function AvatarUpload({ currentAvatar, userName, onSuccess }: AvatarUploadProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const user = useAuthStore((state) => state.user);
  const setUser = useAuthStore((state) => state.setUser);

  const uploadMutation = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append('avatar', file);
      return api.patch('/accounts/profile/avatar/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    },
    onSuccess: (response) => {
      const newAvatarUrl = response.data.avatar;
      toast.success('تصویر پروفایل با موفقیت آپلود شد');
      
      // Update user in store
      if (user) {
        const updatedUser = { ...user, avatar: newAvatarUrl };
        setUser(updatedUser);
        localStorage.setItem('user', JSON.stringify(updatedUser));
      }
      
      onSuccess?.(newAvatarUrl);
      handleClose();
    },
    onError: (error: any) => {
      console.error('Avatar upload error:', error);
      if (error.response?.data?.avatar) {
        toast.error(error.response.data.avatar[0]);
      } else {
        toast.error('خطا در آپلود تصویر');
      }
    },
  });

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
      toast.error('لطفا یک فایل تصویری انتخاب کنید');
      return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      toast.error('حجم فایل نباید بیشتر از 5 مگابایت باشد');
      return;
    }

    setSelectedFile(file);

    // Create preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result as string);
    };
    reader.readAsDataURL(file);
  };

  const handleUpload = () => {
    if (!selectedFile) return;
    uploadMutation.mutate(selectedFile);
  };

  const handleClose = () => {
    setIsOpen(false);
    setPreview(null);
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const getInitials = () => {
    return userName
      .split(' ')
      .map((n) => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <>
      <div className="relative inline-block">
        <Avatar className="h-24 w-24 cursor-pointer" onClick={() => setIsOpen(true)}>
          <AvatarImage src={currentAvatar} alt={userName} />
          <AvatarFallback className="text-2xl">{getInitials()}</AvatarFallback>
        </Avatar>
        <button
          onClick={() => setIsOpen(true)}
          className="absolute bottom-0 right-0 p-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition-colors shadow-lg"
          title="تغییر تصویر پروفایل"
        >
          <Camera className="h-4 w-4" />
        </button>
      </div>

      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>تغییر تصویر پروفایل</DialogTitle>
            <DialogDescription>
              یک تصویر برای پروفایل خود انتخاب کنید (حداکثر 5 مگابایت)
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 py-4">
            {/* Preview */}
            <div className="flex justify-center">
              <Avatar className="h-32 w-32">
                <AvatarImage src={preview || currentAvatar} alt={userName} />
                <AvatarFallback className="text-4xl">{getInitials()}</AvatarFallback>
              </Avatar>
            </div>

            {/* File Input */}
            <div className="flex flex-col gap-2">
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                className="hidden"
                id="avatar-upload"
              />
              <label
                htmlFor="avatar-upload"
                className="flex items-center justify-center gap-2 px-4 py-2 border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-lg cursor-pointer hover:border-blue-500 dark:hover:border-blue-400 transition-colors"
              >
                <Upload className="h-5 w-5" />
                <span className="text-sm">
                  {selectedFile ? selectedFile.name : 'انتخاب تصویر'}
                </span>
              </label>

              {selectedFile && (
                <div className="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-900 rounded">
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    حجم: {(selectedFile.size / 1024).toFixed(2)} کیلوبایت
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => {
                      setSelectedFile(null);
                      setPreview(null);
                      if (fileInputRef.current) {
                        fileInputRef.current.value = '';
                      }
                    }}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              )}
            </div>

            {/* Info */}
            <div className="text-xs text-gray-500 dark:text-gray-400">
              <p>• فرمت‌های مجاز: JPG, PNG, GIF, WebP</p>
              <p>• حداکثر حجم: 5 مگابایت</p>
              <p>• توصیه می‌شود از تصاویر مربع استفاده کنید</p>
            </div>
          </div>

          <DialogFooter>
            <Button variant="outline" onClick={handleClose} disabled={uploadMutation.isPending}>
              انصراف
            </Button>
            <Button
              onClick={handleUpload}
              disabled={!selectedFile || uploadMutation.isPending}
            >
              {uploadMutation.isPending ? (
                <>
                  <Loader2 className="ml-2 h-4 w-4 animate-spin" />
                  در حال آپلود...
                </>
              ) : (
                'آپلود'
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
