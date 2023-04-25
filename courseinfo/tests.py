from django.test import TestCase
from django.urls import reverse, resolve
from courseinfo.models import Period, Year, Semester, Course, Instructor, Student, Section, Registration
from courseinfo.views import (
    InstructorList,
    InstructorDetail,
    SectionList,
    SectionDetail,
    CourseList,
    CourseDetail,
    SemesterList,
    SemesterDetail,
    StudentList,
    StudentDetail,
    RegistrationList,
    RegistrationDetail
)


class PeriodModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.period = Period.objects.create(period_sequence=1, period_name='Winter')

    def test_str_method(self):
        self.assertEqual(str(self.period), 'Winter')

    def test_ordering(self):
        self.assertEqual(Period.objects.first(), self.period)


class YearModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.year = Year.objects.create(year=2023)

    def test_str_method(self):
        self.assertEqual(str(self.year), '2023')

    def test_ordering(self):
        self.assertEqual(Year.objects.first(), self.year)


class InstructorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.instructor = Instructor.objects.create(first_name='Qiaoyue', last_name='Sun')

    # test for models
    def test_str_method(self):
        self.assertEqual(str(self.instructor), 'Sun, Qiaoyue')

    def test_ordering(self):
        self.assertEqual(Instructor.objects.first(), self.instructor)

    def test_unique_together_constraint(self):
        with self.assertRaises(Exception):
            Instructor.objects.create(first_name='Qiaoyue', last_name='Sun')

    # test for list pages
    def test_list_url_exists_at_correct_location(self):
        response = self.client.get("/instructor/")
        self.assertEquals(response.status_code, 200)

    def test_instructor_list_view(self):
        response = self.client.get("/instructor/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courseinfo/instructor_list.html')

    # test for detail pages
    def test_detail_url_exists_at_correct_location(self):
        url = reverse('courseinfo_instructor_detail_urlpattern', args=[self.instructor.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        no_response = self.client.get("/instructor/100000/")
        self.assertEqual(no_response.status_code, 404)

    def test_instructor_detail_view(self):
        url = reverse('courseinfo_instructor_detail_urlpattern', args=[self.instructor.pk])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "courseinfo/instructor_detail.html")

    # test for link pages:
    def test_get_absolute_url(self):
        expected_url = f'/instructor/{self.instructor.pk}/'
        self.assertEqual(self.instructor.get_absolute_url(), expected_url)

    def test_instructor_list_template(self):
        # Test that the instructor_list template renders correctly
        url = reverse('courseinfo_instructor_list_urlpattern')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courseinfo/instructor_list.html')
        # Test that each instructor is displayed as a link to its detail page
        instructors = response.context['instructor_list']
        for instructor in instructors:
            expected_link = reverse('courseinfo_instructor_detail_urlpattern', kwargs={'pk': instructor.pk})
            self.assertContains(response, f'<a href="{expected_link}">{instructor}</a>')


class SectionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        period = Period.objects.create(period_sequence=1, period_name='Winter')
        year = Year.objects.create(year=2022)
        semester = Semester.objects.create(year=year, period=period)
        course = Course.objects.create(course_number='IS515', course_name='Information Modeling')
        instructor = Instructor.objects.create(first_name='Qiaoyue', last_name='Sun')
        cls.section = Section.objects.create(section_name='01', semester=semester, course=course, instructor=instructor)

    def test_section_name(self):
        section = Section.objects.get(section_id=1)
        expected_section_name = '01'
        self.assertEquals(section.section_name, expected_section_name)

    def test_section_semester(self):
        section = Section.objects.get(section_id=1)
        expected_semester = Semester.objects.get(semester_id=1)
        self.assertEquals(section.semester, expected_semester)

    def test_section_course(self):
        section = Section.objects.get(section_id=1)
        expected_course = Course.objects.get(course_id=1)
        self.assertEquals(section.course, expected_course)

    def test_section_instructor(self):
        section = Section.objects.get(section_id=1)
        expected_instructor = Instructor.objects.get(instructor_id=1)
        self.assertEquals(section.instructor, expected_instructor)

    def test_list_url_exists_at_correct_location(self):
        response = self.client.get("/section/")
        self.assertEquals(response.status_code, 200)

    def test_section_list_view(self):
        response = self.client.get("/section/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courseinfo/section_list.html')

    def test_detail_url_exists_at_correct_location(self):
        url = reverse('courseinfo_section_detail_urlpattern', args=[self.section.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        no_response = self.client.get("/section/100000/")
        self.assertEqual(no_response.status_code, 404)

    def test_section_detail_view(self):
        url = reverse('courseinfo_section_detail_urlpattern', args=[self.section.pk])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "courseinfo/section_detail.html")

    # test for link pages:
    def test_get_absolute_url(self):
        expected_url = f'/section/{self.section.pk}/'
        self.assertEqual(self.section.get_absolute_url(), expected_url)

    def test_section_list_template(self):
        url = reverse('courseinfo_section_list_urlpattern')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courseinfo/section_list.html')
        sections = response.context['section_list']
        for section in sections:
            expected_link = reverse('courseinfo_section_detail_urlpattern', kwargs={'pk': section.pk})
            self.assertContains(response, f'<a href="{expected_link}">{section}</a>')


class CourseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.course = Course.objects.create(course_number='IS507', course_name='Data Stat Info')

    def test_str_method(self):
        self.assertEqual(str(self.course), 'IS507 - Data Stat Info')

    def test_ordering(self):
        self.assertEqual(Course.objects.first(), self.course)

    def test_unique_together_constraint(self):
        with self.assertRaises(Exception):
            Course.objects.create(course_number='IS507', course_name='Data Stat Info')

    def test_list_url_exists_at_correct_location(self):
        response = self.client.get("/course/")
        self.assertEquals(response.status_code, 200)

    def test_course_list_view(self):
        response = self.client.get("/course/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courseinfo/course_list.html')

    def test_detail_url_exists_at_correct_location(self):
        url = reverse('courseinfo_course_detail_urlpattern', args=[self.course.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        no_response = self.client.get("/course/100000/")
        self.assertEqual(no_response.status_code, 404)

    def test_course_detail_view(self):
        url = reverse('courseinfo_course_detail_urlpattern', args=[self.course.pk])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "courseinfo/course_detail.html")

    # test for link pages:
    def test_get_absolute_url(self):
        expected_url = f'/course/{self.course.pk}/'
        self.assertEqual(self.course.get_absolute_url(), expected_url)

    def test_section_list_template(self):
        url = reverse('courseinfo_course_list_urlpattern')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courseinfo/course_list.html')
        courses = response.context['course_list']
        for course in courses:
            expected_link = reverse('courseinfo_course_detail_urlpattern', kwargs={'pk': course.pk})
            self.assertContains(response, f'<a href="{expected_link}">{course}</a>')


class SemesterModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.year = Year.objects.create(year=2023)
        cls.period = Period.objects.create(period_sequence=1, period_name='Winter')
        cls.semester = Semester.objects.create(year=cls.year, period=cls.period)

    def test_str_method(self):
        self.assertEqual(str(self.semester), '2023 - Winter')

    def test_ordering(self):
        self.assertEqual(Semester.objects.first(), self.semester)

    def test_unique_together_constraint(self):
        with self.assertRaises(Exception):
            Semester.objects.create(year=self.year, period=self.period)

    def test_list_url_exists_at_correct_location(self):
        response = self.client.get("/semester/")
        self.assertEquals(response.status_code, 200)

    def test_semester_list_view(self):
        response = self.client.get("/semester/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courseinfo/semester_list.html')

    def test_detail_url_exists_at_correct_location(self):
        url = reverse('courseinfo_semester_detail_urlpattern', args=[self.semester.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        no_response = self.client.get("/semester/100000/")
        self.assertEqual(no_response.status_code, 404)

    def test_semester_detail_view(self):
        url = reverse('courseinfo_semester_detail_urlpattern', args=[self.semester.pk])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "courseinfo/semester_detail.html")

    # test for link pages:
    def test_get_absolute_url(self):
        expected_url = f'/semester/{self.semester.pk}/'
        self.assertEqual(self.semester.get_absolute_url(), expected_url)

    def test_section_list_template(self):
        url = reverse('courseinfo_semester_list_urlpattern')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courseinfo/semester_list.html')
        semesters = response.context['semester_list']
        for semester in semesters:
            expected_link = reverse('courseinfo_semester_detail_urlpattern', kwargs={'pk': semester.pk})
            self.assertContains(response, f'<a href="{expected_link}">{semester}</a>')


class StudentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = Student.objects.create(first_name='Joy', last_name='Sun')

    def test_str_method(self):
        self.assertEqual(str(self.student), 'Sun, Joy')

    def test_ordering(self):
        self.assertEqual(Student.objects.first(), self.student)

    def test_unique_together_constraint(self):
        with self.assertRaises(Exception):
            Student.objects.create(first_name='Joy', last_name='Sun')

    def test_list_url_exists_at_correct_location(self):
        response = self.client.get("/student/")
        self.assertEquals(response.status_code, 200)

    def test_student_list_view(self):
        response = self.client.get("/student/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courseinfo/student_list.html')

    def test_detail_url_exists_at_correct_location(self):
        url = reverse('courseinfo_student_detail_urlpattern', args=[self.student.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        no_response = self.client.get("/student/100000/")
        self.assertEqual(no_response.status_code, 404)

    def test_student_detail_view(self):
        url = reverse('courseinfo_student_detail_urlpattern', args=[self.student.pk])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "courseinfo/student_detail.html")

    # test for link pages:
    def test_get_absolute_url(self):
        expected_url = f'/student/{self.student.pk}/'
        self.assertEqual(self.student.get_absolute_url(), expected_url)

    def test_section_list_template(self):
        url = reverse('courseinfo_student_list_urlpattern')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courseinfo/student_list.html')
        students = response.context['student_list']
        for student in students:
            expected_link = reverse('courseinfo_student_detail_urlpattern', kwargs={'pk': student.pk})
            self.assertContains(response, f'<a href="{expected_link}">{student}</a>')


class RegistrationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        period = Period.objects.create(period_sequence=2, period_name='Spring')
        year = Year.objects.create(year=2022)
        semester = Semester.objects.create(year=year, period=period)
        course = Course.objects.create(course_number='IS515', course_name='Information Modeling')
        instructor = Instructor.objects.create(first_name='Qiaoyue', last_name='Sun')
        section = Section.objects.create(section_name='01', semester=semester, course=course, instructor=instructor)
        student = Student.objects.create(first_name='Joy', last_name='Sun')
        cls.registration = Registration.objects.create(student=student, section=section)

    def test_registration_student(self):
        registration = Registration.objects.get(registration_id=1)
        expected_student = Student.objects.get(student_id=1)
        self.assertEquals(registration.student, expected_student)

    def test_registration_section(self):
        registration = Registration.objects.get(registration_id=1)
        expected_section = Section.objects.get(section_id=1)
        self.assertEquals(registration.section, expected_section)

    def test_list_url_exists_at_correct_location(self):
        response = self.client.get("/registration/")
        self.assertEquals(response.status_code, 200)

    def test_registration_list_view(self):
        response = self.client.get("/registration/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courseinfo/registration_list.html')

    def test_detail_url_exists_at_correct_location(self):
        url = reverse('courseinfo_registration_detail_urlpattern', args=[self.registration.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        no_response = self.client.get("/registration/100000/")
        self.assertEqual(no_response.status_code, 404)

    def test_registration_detail_view(self):
        url = reverse('courseinfo_registration_detail_urlpattern', args=[self.registration.pk])
        response = self.client.get(url)
        self.assertTemplateUsed(response, "courseinfo/registration_detail.html")

    # test for link pages:
    def test_get_absolute_url(self):
        expected_url = f'/registration/{self.registration.pk}/'
        self.assertEqual(self.registration.get_absolute_url(), expected_url)

    def test_section_list_template(self):
        url = reverse('courseinfo_registration_list_urlpattern')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courseinfo/registration_list.html')
        registrations = response.context['registration_list']
        for registration in registrations:
            expected_link = reverse('courseinfo_registration_detail_urlpattern', kwargs={'pk': registration.pk})
            self.assertContains(response, f'<a href="{expected_link}">{registration}</a>')
