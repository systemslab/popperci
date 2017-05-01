import uuid

def demo_tables():
    db.project.truncate()
    db.build.truncate()
    db.experiment.truncate()
    db.validation.truncate()
    db.commit()

    # ================ systemslab/malacology-popper =============
    db.project.insert(project_name="systemslab/malacology-popper",
                      result_id=uuid.uuid4(),
                      workspace='~/malacology-popper/workspace')

    db.build.insert(user_id=auth.user.id,
                    project="systemslab/malacology-popper",
                    meta=p1 + sha1_3[0] + p2 + sha1_3[3] + p3 + sha1_3[2] + p4 + sha1_3[1] + p5,
                    status='Done'
                    )
    db.build.insert(user_id=auth.user.id,
                    project="systemslab/malacology-popper",
                    meta=p1 + sha1_2[0] + p2 + sha1_2[3] + p3 + sha1_2[2] + p4 + sha1_2[1] + p5,
                    status='Done'
                    )
    db.build.insert(user_id=auth.user.id,
                    project="systemslab/malacology-popper",
                    meta=p1 + sha1_1[0] + p2 + sha1_1[3] + p3 + sha1_1[2] + p4 + sha1_1[1] + p5,
                    status='Running'
                    )

    db.experiment.insert(
        experiment_name='Experiment 1 for build 1 on systemslab/malacology-popper',
        build_id=1,
        status='FAIL')
    db.experiment.insert(
        experiment_name='Experiment 2 for build 1 on systemslab/malacology-popper',
        build_id=1,
        status='FAIL')
    db.experiment.insert(
        experiment_name='Experiment 3 for build 1 on systemslab/malacology-popper',
        build_id=1,
        status='FAIL')
    db.experiment.insert(
        experiment_name='Experiment 4 for build 2 on systemslab/malacology-popper',
        build_id=2,
        status='OK')
    db.experiment.insert(
        experiment_name='Experiment 5 for build 2 on systemslab/malacology-popper',
        build_id=2,
        status='GOLD')
    db.experiment.insert(
        experiment_name='Experiment 6 for build 3 on systemslab/malacology-popper',
        build_id=3,
        status='OK')
    db.experiment.insert(
        experiment_name='Experiment 7 for build 3 on systemslab/malacology-popper',
        build_id=3,
        status='GOLD')

    db.validation.insert(
        validation_name='Validation 1 for experiment 1 on systemslab/malacology-popper',
        experiment_id=1,
        validation_id=str(uuid.uuid4()),
        validation="Successful validation for experiment 1",
        status='pass')
    db.validation.insert(
        validation_name='Validation 2 for experiment 1 on systemslab/malacology-popper',
        experiment_id=1,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 1",
        status='fail')
    db.validation.insert(
        validation_name='Validation 3 for experiment 2 on systemslab/malacology-popper',
        experiment_id=2,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 2",
        status='fail')
    db.validation.insert(
        validation_name='Validation 4 for experiment 2 on systemslab/malacology-popper',
        experiment_id=2,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 3",
        status='fail')
    db.validation.insert(
        validation_name='Validation 5 for experiment 3 on systemslab/malacology-popper',
        experiment_id=3,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 3",
        status='pass')
    db.validation.insert(
        validation_name='Validation 6 for experiment 3 on systemslab/malacology-popper',
        experiment_id=3,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 3",
        status='fail')
    db.validation.insert(
        validation_name='Validation 7 for experiment 4 on systemslab/malacology-popper',
        experiment_id=4,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 4",
        status='fail')
    db.validation.insert(
        validation_name='Validation 8 for experiment 4 on systemslab/malacology-popper',
        experiment_id=4,
        validation_id=str(uuid.uuid4()),
        validation="Successful validation for experiment 4",
        status='pass')
    db.validation.insert(
        validation_name='Validation 9 for experiment 5 on systemslab/malacology-popper',
        experiment_id=5,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 5",
        status='pass')
    db.validation.insert(
        validation_name='Validation 10 for experiment 5 on systemslab/malacology-popper',
        experiment_id=5,
        validation_id=str(uuid.uuid4()),
        validation="Successful validation for experiment 5",
        status='pass')
    db.validation.insert(
        validation_name='Validation 11 for experiment 6 on systemslab/malacology-popper',
        experiment_id=6,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 6",
        status='fail')
    db.validation.insert(
        validation_name='Validation 12 for experiment 6 on systemslab/malacology-popper',
        experiment_id=6,
        validation_id=str(uuid.uuid4()),
        validation="Successful validation for experiment 6",
        status='pass')
    db.validation.insert(
        validation_name='Validation 13 for experiment 7 on systemslab/malacology-popper',
        experiment_id=7,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 6",
        status='pass')
    db.validation.insert(
        validation_name='Validation 14 for experiment 7 on systemslab/malacology-popper',
        experiment_id=7,
        validation_id=str(uuid.uuid4()),
        validation="Successful validation for experiment 7",
        status='pass')

    # ================ systemslab/mantle-popper =============
    db.project.insert(project_name="systemslab/mantle-popper",
                      result_id=uuid.uuid4(),
                      workspace='~/mantle-popper/workspace')

    db.build.insert(user_id=auth.user.id,
                    project="systemslab/mantle-popper",
                    meta=p1 + sha1_6[0] + p2 + sha1_6[3] + p3 + sha1_6[2] + p4 + sha1_6[1] + p5,
                    status='Done'
                    )
    db.build.insert(user_id=auth.user.id,
                    project="systemslab/mantle-popper",
                    meta=p1 + sha1_5[0] + p2 + sha1_5[3] + p3 + sha1_5[2] + p4 + sha1_5[1] + p5,
                    status='Done'
                    )
    db.build.insert(user_id=auth.user.id,
                    project="systemslab/mantle-popper",
                    meta=p1 + sha1_4[0] + p2 + sha1_4[3] + p3 + sha1_4[2] + p4 + sha1_4[1] + p5,
                    status='Done'
                    )
    db.experiment.insert(
        experiment_name='Experiment 1 for build 1 on systemslab/mantle-popper',
        build_id=4,
        status='FAIL')
    db.experiment.insert(
        experiment_name='Experiment 2 for build 1 on systemslab/mantle-popper',
        build_id=4,
        status='FAIL')
    db.experiment.insert(
        experiment_name='Experiment 3 for build 1 on systemslab/mantle-popper',
        build_id=4,
        status='FAIL')
    db.experiment.insert(
        experiment_name='Experiment 4 for build 2 on systemslab/mantle-popper',
        build_id=5,
        status='OK')
    db.experiment.insert(
        experiment_name='Experiment 5 for build 2 on systemslab/mantle-popper',
        build_id=5,
        status='OK')
    db.experiment.insert(
        experiment_name='Experiment 6 for build 3 on systemslab/mantle-popper',
        build_id=6,
        status='FAIL')
    db.experiment.insert(
        experiment_name='Experiment 7 for build 3 on systemslab/mantle-popper',
        build_id=6,
        status='OK')

    db.validation.insert(
        validation_name='Validation 1 for experiment 1 on systemslab/mantle-popper',
        experiment_id=8,
        validation_id=str(uuid.uuid4()),
        validation="Successful validation for experiment 1",
        status='pass')
    db.validation.insert(
        validation_name='Validation 2 for experiment 1 on systemslab/mantle-popper',
        experiment_id=8,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 1",
        status='fail')
    db.validation.insert(
        validation_name='Validation 3 for experiment 2 on systemslab/mantle-popper',
        experiment_id=9,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 2",
        status='fail')
    db.validation.insert(
        validation_name='Validation 4 for experiment 2 on systemslab/mantle-popper',
        experiment_id=9,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 3",
        status='fail')
    db.validation.insert(
        validation_name='Validation 5 for experiment 3 on systemslab/mantle-popper',
        experiment_id=10,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 3",
        status='pass')
    db.validation.insert(
        validation_name='Validation 6 for experiment 3 on systemslab/mantle-popper',
        experiment_id=10,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 3",
        status='fail')
    db.validation.insert(
        validation_name='Validation 7 for experiment 4 on systemslab/mantle-popper',
        experiment_id=11,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 4",
        status='fail')
    db.validation.insert(
        validation_name='Validation 8 for experiment 4 on systemslab/mantle-popper',
        experiment_id=11,
        validation_id=str(uuid.uuid4()),
        validation="Successful validation for experiment 4",
        status='pass')
    db.validation.insert(
        validation_name='Validation 9 for experiment 5 on systemslab/mantle-popper',
        experiment_id=12,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 5",
        status='fail')
    db.validation.insert(
        validation_name='Validation 10 for experiment 5 on systemslab/mantle-popper',
        experiment_id=12,
        validation_id=str(uuid.uuid4()),
        validation="Successful validation for experiment 5",
        status='pass')
    db.validation.insert(
        validation_name='Validation 11 for experiment 6 on systemslab/mantle-popper',
        experiment_id=13,
        validation_id=str(uuid.uuid4()),
        validation="Successful validation for experiment 6",
        status='pass')
    db.validation.insert(
        validation_name='Validation 12 for experiment 6 on systemslab/mantle-popper',
        experiment_id=13,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 6",
        status='fail')
    db.validation.insert(
        validation_name='Validation 13 for experiment 7 on systemslab/mantle-popper',
        experiment_id=14,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 6",
        status='fail')
    db.validation.insert(
        validation_name='Validation 14 for experiment 7 on systemslab/mantle-popper',
        experiment_id=14,
        validation_id=str(uuid.uuid4()),
        validation="Successful validation for experiment 7",
        status='pass')


    # ================ ivotron/quiho =============
    db.project.insert(project_name="ivotron/quiho",
                      result_id=uuid.uuid4(),
                      workspace='~/quiho/workspace')
    db.build.insert(user_id=auth.user.id,
                    project="ivotron/quiho",
                    meta=p1 + sha1_9[0] + p2 + sha1_9[3] + p3 + sha1_9[2] + p4 + sha1_9[1] + p5,
                    status='Done'
                    )
    db.build.insert(user_id=auth.user.id,
                    project="ivotron/quiho",
                    meta=p1 + sha1_8[0] + p2 + sha1_8[3] + p3 + sha1_8[2] + p4 + sha1_8[1] + p5,
                    status='Done'
                    )
    db.build.insert(user_id=auth.user.id,
                    project="ivotron/quiho",
                    meta=p1 + sha1_7[0] + p2 + sha1_7[3] + p3 + sha1_7[2] + p4 + sha1_7[1] + p5,
                    status='Done'
                    )
    db.experiment.insert(
        experiment_name='Experiment 1 for build 1 on ivotron/quiho',
        build_id=7,
        status='FAIL')
    db.experiment.insert(
        experiment_name='Experiment 2 for build 1 on ivotron/quiho',
        build_id=7,
        status='FAIL')
    db.experiment.insert(
        experiment_name='Experiment 3 for build 1 on ivotron/quiho',
        build_id=7,
        status='FAIL')
    db.experiment.insert(
        experiment_name='Experiment 4 for build 2 on ivotron/quiho',
        build_id=8,
        status='OK')
    db.experiment.insert(
        experiment_name='Experiment 5 for build 2 on ivotron/quiho',
        build_id=8,
        status='OK')
    db.experiment.insert(
        experiment_name='Experiment 6 for build 3 on ivotron/quiho',
        build_id=9,
        status='OK')
    db.experiment.insert(
        experiment_name='Experiment 7 for build 3 on ivotron/quiho',
        build_id=9,
        status='FAIL')

    db.validation.insert(
        validation_name='Validation 1 for experiment 1 on ivotron/quiho',
        experiment_id=15,
        validation_id=str(uuid.uuid4()),
        validation="Successful validation for experiment 1",
        status='pass')
    db.validation.insert(
        validation_name='Validation 2 for experiment 1 on ivotron/quiho',
        experiment_id=15,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 1",
        status='fail')
    db.validation.insert(
        validation_name='Validation 3 for experiment 2 on ivotron/quiho',
        experiment_id=16,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 2",
        status='fail')
    db.validation.insert(
        validation_name='Validation 4 for experiment 2 on ivotron/quiho',
        experiment_id=16,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 3",
        status='fail')
    db.validation.insert(
        validation_name='Validation 5 for experiment 3 on ivotron/quiho',
        experiment_id=17,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 3",
        status='pass')
    db.validation.insert(
        validation_name='Validation 6 for experiment 3 on ivotron/quiho',
        experiment_id=17,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 3",
        status='fail')
    db.validation.insert(
        validation_name='Validation 7 for experiment 4 on ivotron/quiho',
        experiment_id=18,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 4",
        status='fail')
    db.validation.insert(
        validation_name='Validation 8 for experiment 4 on ivotron/quiho',
        experiment_id=18,
        validation_id=str(uuid.uuid4()),
        validation="Successful validation for experiment 4",
        status='pass')
    db.validation.insert(
        validation_name='Validation 9 for experiment 5 on ivotron/quiho',
        experiment_id=19,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 5",
        status='fail')
    db.validation.insert(
        validation_name='Validation 10 for experiment 5 on ivotron/quiho',
        experiment_id=19,
        validation_id=str(uuid.uuid4()),
        validation="Successful validation for experiment 5",
        status='pass')
    db.validation.insert(
        validation_name='Validation 11 for experiment 6 on ivotron/quiho',
        experiment_id=20,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 6",
        status='fail')
    db.validation.insert(
        validation_name='Validation 12 for experiment 6 on ivotron/quiho',
        experiment_id=20,
        validation_id=str(uuid.uuid4()),
        validation="Successful validation for experiment 6",
        status='pass')
    db.validation.insert(
        validation_name='Validation 13 for experiment 7 on ivotron/quiho',
        experiment_id=21,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 6",
        status='fail')
    db.validation.insert(
        validation_name='Validation 14 for experiment 7 on ivotron/quiho',
        experiment_id=21,
        validation_id=str(uuid.uuid4()),
        validation="Failed validation for experiment 7",
        status='fail')
