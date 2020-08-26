from io import BytesIO
from tempfile import NamedTemporaryFile
from PIL import Image

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from .models import Post


class TestGeneral(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.client = Client()
        self.User.objects.create_user(username="User_1", password="2222222")
        self.User.objects.create_user(username="User_2", password="2222222")
        self.user_2 = self.User.objects.get(username="User_2")
        self.user = self.User.objects.get(username="User_1")
        self.client.force_login(self.user)
        self.post_count = Post.objects.count()
        self.post = Post.objects.create(
            text="uni_some_text",
            author=self.user,
            id="999"
        )
        self.url_index = reverse("index")
        self.url_profile = reverse("profile", args=[self.user])
        self.url_post = reverse("post", args=[self.user, self.post.id])
        self.url_edit = reverse("post_edit", args=[self.user, self.post.id])
        self.url_comment = reverse("add_comment",
                                   args=[self.user, self.post.id]
                                   )
        self.urls = [self.url_index, self.url_profile, self.url_post]

    def test_user_profile(self):
        """
        Проверка на создание профиля нового пользователя.
        """
        resp = self.client.get(self.url_post)
        self.assertEqual(
            resp.status_code,
            200,
            msg="проверка на создание профиля пользователя")

    def test_user_can_make_post(self):
        """
        Авторизованный пользователь может опубликовать пост.
        """
        self.client.post(reverse("new_post"), {"text": "new_post_uniq_2123"})
        response = Post.objects.filter(text="new_post_uniq_2123")
        self.assertTrue(response, True)

    def test_show_post(self):
        """
        Проверка, пост должен появится на всех страницах.
        """
        cache.clear()
        for url in self.urls:
            response = self.client.get(url)
            self.assertContains(response, "uni_some_text")

    def post_edit_test(self):
        """
        Проверка на возможность редактированне поста.
        """
        self.client.post(self.url_edit,
                         {"text": "New_post_edited"}
                         )
        for url in self.urls:
            response = self.client.get(url)
            self.assertContains(response, "New_post_edited")

    def test_non_auth_user_can_make_post(self):
        """
        Не авторизованный пользователь получит редирект на страницу
        авторизации.
        """
        self.client.logout()
        response = self.client.post(reverse("new_post"),
                                    {"text": "I_love_anime"},
                                    follow=True
                                    )
        self.assertRedirects(
            response,
            "/auth/login/?next=/new", )
        response = Post.objects.filter(text="I_love_anime")
        self.assertFalse(response, False)

    def test_404_error(self):
        """
        Тест на работоспособность ошибки 404, в первый get запрос передан
        заведомо неверный URL, а во второй передан верный URL.
        """
        response = self.client.get("/new/leo")
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/new")
        self.assertEqual(response.status_code, 200)

    def test_cache(self):
        self.client.get(reverse("index"))
        self.client.post(reverse("new_post"), {"text": "teeeeext"})
        response1 = self.client.get(reverse("index"))
        self.assertNotContains(response1, "teeeeext")

    def test_image_tag(self):
        cache.clear()
        temp = NamedTemporaryFile()
        img_data = BytesIO()
        image = Image.new("RGB", size=(10, 10), color=(255, 0, 0, 0))
        image.save(img_data, format='JPEG')
        image = SimpleUploadedFile(
            temp.name + '.jpg',
            img_data.getvalue(),
            'image/png'
        )
        cache.clear()
        self.client.post(self.url_edit,
                         {"text": "New_post_edited",
                          "image": image},
                         follow=True
                         )
        for url in self.urls:
            response = self.client.get(url)
            self.assertContains(response, '<img')

    def test_image_protect(self):
        """
        Тест на правильность работы защиты от непарвильного формата.
        """
        response = self.client.post(reverse("new_post"),
                                    {"text": "text_random",
                                     "image": SimpleUploadedFile('generated.txt',
                                                                 b'not image text'), }
                                    )
        error = "Загрузите правильное изображение." \
                " Файл, который вы загрузили, " \
                "поврежден или не является изображением."
        self.assertFormError(response, "form", 'image', error)

    def test_page_follow(self):
        """Тест работы follow_page."""
        Post.objects.create(
            text="some_text",
            author=self.user_2,
        )
        self.client.get(reverse("profile_follow", args=[self.user_2]))
        response = self.client.get(reverse("follow_index"))
        self.assertContains(response, "some_text")

    def test_auth_can_make_comm(self):
        """Тест на праивльность работы кометариев для
        авторизованного пользователя и не авторизованного."""
        self.client.post(self.url_comment, {"text": "test_comment"})
        response = self.client.get(self.url_post)
        self.assertContains(response, "test_comment")
        self.client.logout()
        self.client.post(self.url_comment, {"text": "test_comment_non_auth"})
        response = self.client.get(self.url_post)
        self.assertNotContains(response, "test_comment_non_auth")


class TestSubGanaral(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.client = Client()
        self.User.objects.create_user(username="User_1", password="2222222")
        self.User.objects.create_user(username="User_2", password="2222222")
        self.user_2 = self.User.objects.get(username="User_2")
        self.user = self.User.objects.get(username="User_1")
        self.client.force_login(self.user)
        self.post_count = Post.objects.count()
        self.post = Post.objects.create(
            text="uni_some_text",
            author=self.user,
            id="999"
        )
        self.url_comment = reverse("add_comment",
                                   args=[self.user, self.post.id]
                                   )

    def test_auth_can_make_sub(self):
        """Тест на праивльность работы кометариев для
        авторизованного пользователя."""
        sub_count_1 = self.user_2.following.all().count()
        self.client.get(reverse("profile_follow", args=[self.user_2]))
        sub_count_2 = self.user_2.following.all().count()
        self.assertNotEqual(sub_count_1, sub_count_2)
        self.client.get(reverse("profile_unfollow", args=[self.user_2]))

    def test_non_auth_cant_make_sub(self):
        self.client.logout()
        sub_count_1 = self.user_2.following.all().count()
        self.client.get(reverse("profile_unfollow", args=[self.user_2]))
        sub_count_3 = self.user_2.following.all().count()
        self.assertEqual(sub_count_1, sub_count_3)
