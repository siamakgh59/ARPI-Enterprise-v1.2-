        # Coin Bubble

        bubble = data.get(
            "coin_bubble"
        )

        if bubble is not None:

            try:

                bubble_value = float(
                    bubble
                )


                # Normalize raw bubble value
                # Faraz raw parser output calibration

                if bubble_value > 1000:

                    normalized_bubble = (
                        bubble_value / 100
                    )

                else:

                    normalized_bubble = bubble_value



                if normalized_bubble > 20:

                    scores[
                        "coin_bubble"
                    ] = 30

                    risks.append(
                        "High coin bubble risk"
                    )


                elif normalized_bubble > 10:

                    scores[
                        "coin_bubble"
                    ] = 50

                    risks.append(
                        "Medium coin bubble risk"
                    )


                else:

                    scores[
                        "coin_bubble"
                    ] = 70


            except Exception:

                scores[
                    "coin_bubble"
                ] = 50


        else:

            scores[
                "coin_bubble"
            ] = 50
