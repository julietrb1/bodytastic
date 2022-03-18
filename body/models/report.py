from django.conf import settings
from django.db import models
from django.urls import reverse_lazy

BRA_CUP_NAMES = ("A", "B", "C", "D", "E", "F", "G")
BRA_CUP_STARTING_BAND_A_CUP_LOWER_CM = 77
BRA_CUP_JUMP_CUP_CM = 2
BRA_CUP_JUMP_BAND_CM = 5
BRA_BAND_SIZE_JUMP_CM = 6
BRA_BAND_SIZE_STARTING_UPPER_CM = 70
BRA_BAND_SIZE_STARTING_BAND = 8
BRA_BAND_SIZE_ENDING_BAND = 22
BRA_BAND_COMBOS = tuple(
    (
        (BRA_BAND_SIZE_STARTING_UPPER_CM + BRA_BAND_SIZE_JUMP_CM * idx, band_size)
        for (idx, band_size) in enumerate(
            range(BRA_BAND_SIZE_STARTING_BAND, BRA_BAND_SIZE_ENDING_BAND + 1, 2)
        )
    )
)


class Report(models.Model):
    """A general body check-in by a user on a given date."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    when = models.DateField()
    weight_in_kg = models.DecimalField(
        verbose_name="Weight (kg)",
        decimal_places=2,
        max_digits=5,
        null=True,
        blank=True,
    )
    attributes = models.ManyToManyField("Attribute", blank=True)

    class Meta:
        ordering = ["-when"]
        unique_together = [["user", "when"]]
        db_table = "report"

    def __str__(self):
        return f"{self.user} on {self.when}"

    def get_absolute_url(self):
        return reverse_lazy("report-detail", kwargs={"pk": self.pk})

    @property
    def weight_display(self):
        if not self.weight_in_kg:
            return "no weight"
        return f"{float(self.weight_in_kg):g} kg"

    def __get_measurement(self, body_area_name):
        entry = self.entry_set.filter(body_area__name=body_area_name).first()
        return entry.measurement if entry else None

    @property
    def waist_measurement(self):
        return self.__get_measurement("Waist")

    @property
    def hips_measurement(self):
        return self.__get_measurement("Hips")

    @property
    def bust_measurement(self):
        return self.__get_measurement("Bust")

    @property
    def under_bust_measurement(self):
        return self.__get_measurement("Under bust")

    @property
    def waist_hip_ratio(self):
        waist_measurement = self.waist_measurement
        hips_measurement = self.hips_measurement

        if not waist_measurement or not hips_measurement:
            return None

        return waist_measurement / hips_measurement

    @staticmethod
    def _band_from_under_bust(under_bust_measurement):
        if (
            under_bust_measurement
            <= BRA_BAND_SIZE_STARTING_UPPER_CM - BRA_BAND_SIZE_JUMP_CM
        ):
            # Band size too small
            return None

        for upper_cm, band_size in BRA_BAND_COMBOS:
            if under_bust_measurement <= upper_cm:
                return band_size

        return None

    @staticmethod
    def _lower_cm_for_band(band_size):
        return (
            BRA_CUP_STARTING_BAND_A_CUP_LOWER_CM
            + (band_size / 2 - 4) * BRA_CUP_JUMP_BAND_CM
        )

    @staticmethod
    def _cup_size(band_size, bust_measurement):
        lower_cm_for_band = Report._lower_cm_for_band(band_size)
        for idx, cup_name in enumerate(BRA_CUP_NAMES):
            lower_incl_cm_with_cup = lower_cm_for_band + BRA_CUP_JUMP_CUP_CM * idx
            upper_excl_cm_with_cup = lower_incl_cm_with_cup + BRA_CUP_JUMP_CUP_CM

            if bust_measurement < lower_incl_cm_with_cup:
                return "AA"

            if (
                bust_measurement >= lower_incl_cm_with_cup
                and bust_measurement < upper_excl_cm_with_cup
            ):
                return cup_name

    @property
    def bra_size(self):
        bust_measurement = self.bust_measurement
        under_bust_measurement = self.under_bust_measurement

        if not bust_measurement or not under_bust_measurement:
            return None

        band_size = self._band_from_under_bust(under_bust_measurement)
        if not band_size:
            return None

        cup_size = self._cup_size(band_size, bust_measurement)
        if not cup_size:
            return None

        return f"{band_size}{cup_size}"
